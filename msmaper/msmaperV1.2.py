# -*- coding:utf-8 -*-
import nmap
import sys
import os
import platform
import subprocess
import json
import argparse
import random
import multiprocessing

args = dict()

def cmdLineParser():
    parser = argparse.ArgumentParser(description='Msmaper',
                                     usage='python msmaperV1.0.py -file ip.txt',
                                     add_help=False)

    useage = parser.add_argument_group('Usage')

    useage.add_argument('-file', metavar='file', dest="targetFile", type=str, default='',
                        help='load targets from file (e.g. ip.txt)')
    useage.add_argument('-p', metavar='num', dest="process", type=int, default=10,
                        help='nmap scan process, 10 by default')
    useage.add_argument('-ports', metavar='ports', dest="ports", type=str,
                        help='scan ports,no default, eg: 21,22-100')
    useage.add_argument('-rate', metavar='rate', dest="rate", type=int,default=2000,
                        help='masscan rate, default: 2000')
    useage.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args.update(vars(parser.parse_args()))

def checkEnv():
    if sys.version.split()[0] >= "3":
        exit('[-] Python 2.7 is required ')
    if platform.system() == 'Windows':
        print('[-] Your system is windows , it is recommended to use linux ')
    if not os.path.exists('data'):os.mkdir('data')
    if not os.path.exists('output'): os.mkdir('output')

class msMap():
    def __init__(self):
        self.jsonfile = 'data/default.json'
        self.scanports = '21,22,80,8888'
        self.output = 'output/default.txt'
        self.lock = multiprocessing.Lock()
        self.portsInfo = {}
        self.q = multiprocessing.Manager().Queue()
        self.result = multiprocessing.Manager().Queue()

    def masscan(self):
        self.jsonfile = 'data/{}_portinfo.json'.format(random.randint(10000,99999))
        self.output = self.jsonfile.replace('.json','.txt').replace('data','output')
        if not args['targetFile']:
            print '[-] no input file'
            sys.exit(-3)
        if args['ports']:
            self.scanports = args['ports']
        # p = subprocess.Popen(['masscan','-iL',args['targetFile'],'-p',self.scanports,'-oJ',self.jsonfile],shell=True)
        # p.wait()
        mscanLine = 'masscan -iL {} -p{} -oJ {} --rate {}'.format(args['targetFile'],self.scanports,
                                                                  self.jsonfile,str(args['rate']))
        os.system(mscanLine)

    def parseJson(self):
        for line in open(self.jsonfile,'r'):
            try:
                if line.strip().startswith('{'):
                    ports = []
                    line = line.strip().replace(' ','').strip(',')
                    #print line
                    ipObj = json.loads(line)
                    ip = ipObj['ip']
                    port = ipObj['ports'][0]['port']
                    if ip not in self.portsInfo.keys():
                        ports.append(port)
                        self.portsInfo[ip] = ports
                    else:
                        if port not in self.portsInfo[ip]:
                            self.portsInfo[ip].append(port)
            except:
                pass
        for k in self.portsInfo.keys():
            self.q.put('{}|{}'.format(k,','.join(str(s) for s in self.portsInfo[k])))

    def nmapRun(self):
        while not self.q.empty():
            target = self.q.get(block=False,timeout=0.5)
            ip = target.split('|')[0]
            ports = target.split('|')[1]
            nm = nmap.PortScanner()

            try:
                ret = nm.scan(ip, ports, arguments='-T4 -Pn -n -sV')
                for i in ret['scan'][ip]['tcp'].keys():
                    retval = '{}\t{}\t{}\t{} {}'.format(ip,str(i),ret['scan'][ip]['tcp'][int(i)]['name'],
                                                     ret['scan'][ip]['tcp'][int(i)]['product'],
                                                     ret['scan'][ip]['tcp'][int(i)]['version'])
                    self.outfile(retval)
            except:
                try:
                    ret = nm.scan(ip, ports, arguments='-T4 -Pn -n -sV')
                    for i in ret['scan'][ip]['tcp'].keys():
                        retval = '{}\t{}\t{}\t{} {}'.format(ip, str(i), ret['scan'][ip]['tcp'][int(i)]['name'],
                                                         ret['scan'][ip]['tcp'][int(i)]['product'],
                                                         ret['scan'][ip]['tcp'][int(i)]['version'])
                        self.outfile(retval)
                except:
                    pass

    def outfile(self,s):
        self.lock.acquire()
        with open(self.output,'a+') as f:
            f.write(s+'\n')
        self.lock.release()

    def bannerScan(self):
        pool = []
        for i in range(args['process']):
            p = multiprocessing.Process(target=self.nmapRun,args=())
            p.start()
            pool.append(p)
            pass
        while True:
            for p in pool:
                if not p.is_alive():
                    pool.remove(p)
            if not pool:
                break

    def run(self):
        self.masscan()
        self.parseJson()
        self.bannerScan()

def main():
    checkEnv()
    cmdLineParser()
    m = msMap()
    m.run()
    sys.exit(0)

if __name__ == '__main__':
    main()
