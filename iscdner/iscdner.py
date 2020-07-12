# -*- coding:utf-8 -*-
import dns.resolver
import os
import sys

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

    if len(ipList)>2:
        with open('result.txt','a+') as f:
            line = site + '\t' + 'CDN' + '\t' + ','.join(ipList)
            f.write(line + '\n')
            print line
    elif len(ipList)<=2:
        with open('result.txt','a+') as f:
            line = site + '\t' + 'noCDN' + '\t' + ','.join(ipList)
            f.write(line + '\n')
            print line
    else:
        with open('result.txt','a+') as f:
            line = site + '\t' + 'error'
            f.write(line + '\n')
            print line

if __name__ == '__main__':
    open('result.txt','a+').truncate()
    if os.path.isfile(sys.argv[1]):
        for line in open(sys.argv[1],'r+').readlines():
            dnsQuery(line.strip())
    else:
        dnsQuery(sys.argv[1].strip())
