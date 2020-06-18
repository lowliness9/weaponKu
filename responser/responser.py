#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse
import sys
import time
import Queue
import threading
import requests
from time import sleep
requests.packages.urllib3.disable_warnings()

args = dict()

aRule = []

q = Queue.Queue()

lock = threading.Lock()

outputFile = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.txt'

commonHeaders = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Connection':'close'
}

def cmdLineParser():
    parser = argparse.ArgumentParser(description='2020',
                                     usage='python vMather.py --file file.txt',
                                     add_help=False)

    useage = parser.add_argument_group('Usage')

    useage.add_argument('-u', metavar='TARGET', dest="targetUrl", type=str, default='',
                        help="test a single target (e.g. www.example.com)")
    useage.add_argument('--file', metavar='FILE', dest="targetFile", type=str, default='',
                        help='load targets from targetFile (e.g. ip.txt)')
    useage.add_argument('-t', metavar='NUM', dest="threadNum", type=int, default=5,
                        help='num of threads/concurrent, 5 by default')
    useage.add_argument('-s', metavar='NUM', dest="timeout", type=int, default=5,
                        help='timeout setting, 5s by default')
    useage.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args.update(vars(parser.parse_args()))

def msg(var):
    localtime = time.strftime("%m/%d %H:%M:%S", time.localtime())
    print '[+] {} {}'.format(localtime,var)

def loadRules():
    rules = open('rule.conf','r+').readlines()
    for rule in rules:
        if not rule.strip().startswith('#') and rule.strip() != '' and len(rule.strip().split('\t')) >=2:
            aRule.append(rule.strip().split('\t'))
    msg('Rules count:{} .'.format(len(aRule)))
    sleep(1)


def loadTargets():
    for line in open(args['targetFile'], 'r+').readlines():
        if line.strip() != '':
            q.put(parseHost(line))
    msg('Host count:{} .'.format(q.qsize()))
    sleep(1)

def parseHost(host):
    host = host.strip()
    if '://' in host:
        return host
    else:
        return 'http://' + host


def mul():
    loadTargets()
    pool = []
    for _ in range(args['threadNum']):
        t = threading.Thread(target=run,args=())
        t.start()
        pool.append(t)
    while True:
        for t in pool:
            if not t.is_alive():
                pool.remove(t)
        if not pool:
            break

def writeOutput(result):
    try:
        lock.acquire()
        with open(outputFile,'a+') as f:
            for line in result:
                f.write(line+'\n')
        lock.release()
    except:
        lock.release()

def run():
    while not q.empty():
        url = q.get(block=False,timeout=0.5)
        lock.acquire()
        msg('Remaining:{},Working:{}'.format(q.qsize(),url))
        lock.release()
        try:
            request = requests.get(url = url,headers = commonHeaders,timeout = args['timeout'],verify = False)
            result = []
            for rule in aRule:
                name = rule[0].split(':')[1]
                ok = True
                for i in range(1,len(rule)):
                    matchContent = rule[i].split(':')[1]
                    if matchContent in request.content or matchContent in request.content:
                        pass
                    else:
                        ok = False
                        break
                if ok:
                    result.append(name + ' ' + url)
            if result:
                writeOutput(result)
        except:
            pass

def main():
    cmdLineParser()
    loadRules()
    if args['targetUrl']:
        msg('Function is not implemented .')
    if args['targetFile']:
        mul()
        msg('Finished .')

if __name__ == '__main__':
    main()
