# -*- coding:utf-8 -*-
import dns.resolver
import os
import sys
import re


limit = 2
limitIP = []


def isIP(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

def dnsQuery(site):
    dns_servers = [
        '114.114.114.114',
        '223.5.5.5',
        '180.76.76.76',
        '101.226.4.6',
        '123.125.81.6',
        '8.8.8.8',
        '1.1.1.1'
    ]
    ipList = set()
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
        with open('iscdner.txt','a+') as f:
            line = '{}\tCDN\t{}'.format(site,','.join(ipList))
            f.write(line + '\n')
            print line
    elif 0<len(ipList)<=limit:
        with open('iscdner.txt','a+') as f:
            line = '{}\tnoCDN\t{}'.format(site,','.join(ipList))
            f.write(line + '\n')
            print line
        with open('iscdnerIP.txt','a+') as f:
            for ip in ipList:
                if isIP(ip) and ip.strip() not in limitIP:
                    f.write(ip.strip()+'\n')
                    limitIP.append(ip.strip())
    else:
        with open('iscdner.txt','a+') as f:
            line = site + '\t' + 'error'
            f.write(line + '\n')
            print line

if __name__ == '__main__':
    open('iscdner.txt','a+').truncate()
    open('iscdnerIP.txt', 'a+').truncate()
    if os.path.isfile(sys.argv[1]):
        for line in open(sys.argv[1],'r+').readlines():
            dnsQuery(line.strip())
    else:
        dnsQuery(sys.argv[1].strip())

