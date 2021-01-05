#!/usr/bin/env python
# -*- coding:utf-8 -*-
import dns.resolver
import os
import sys
import re
import Queue
from threading import Thread
from threading import Lock
lock = Lock()
qu = Queue.Queue()

limit = 2

def isIP(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

def dnsQuery():
    dns_servers = [
        # 国内
        '114.114.114.114',
        # 国内阿里云
        '223.5.5.5',
        # 百度DNS
        '180.76.76.76',
        # 国内DNS
        '101.226.4.6',
        # Google DNS
        '8.8.8.8',
        # 阿尔巴尼亚
        '46.252.40.2',
        # 美国DNS
        '1.1.1.1',
        # 瑞士
        # '5.144.17.119',
    ]

    while not qu.empty():
        try:
            site = qu.get(block=False,timeout=0.1)
            ipList = set()
            limitIP = []
            for server in dns_servers:
                try:
                    self_server = dns.resolver.Resolver()
                    self_server.nameservers = [server]
                    query = self_server.query(site)
                    for i in query.response.answer:
                        for x in i.items:
                            ipList.add(str(x))
                except:
                    pass
            if len(ipList)>limit:
                lock.acquire()
                with open('www2IP.txt','a+') as f:
                    line = '{}\tCDN\t{}'.format(site,','.join(ipList))
                    f.write(line + '\n')
                    print line
                lock.release()
            elif 0<len(ipList)<=limit:
                lock.acquire()
                with open('www2IP.txt','a+') as f:
                    line = '{}\tnoCDN\t{}'.format(site,','.join(ipList))
                    f.write(line + '\n')
                    print line
                with open('realIP.txt','a+') as f:
                    for ip in ipList:
                        if isIP(ip) and ip.strip() not in limitIP:
                            f.write(ip.strip()+'\n')
                            limitIP.append(ip.strip())
                lock.release()
            else:
                lock.acquire()
                with open('www2IP.txt','a+') as f:
                    line = site + '\t' + 'error'
                    f.write(line + '\n')
                    print line
                lock.release()
        except Queue.Empty:
            break
        except:
            pass

if __name__ == '__main__':
    open('www2IP.txt','a+').truncate()
    open('realIP.txt', 'a+').truncate()
    if os.path.isfile(sys.argv[1]):
        for line in open(sys.argv[1],'r+').readlines():
            line = line.strip()
            if line:
                qu.put(line)
    else:
        sys.exit(-1)

    pool = [Thread(target=dnsQuery,args=()) for i in range(30)]
    for th in pool:th.start()
    for th in pool:th.join()

