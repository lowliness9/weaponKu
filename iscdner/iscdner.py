# -*- coding:utf-8 -*-
import dns.resolver
import os
import sys
import re

# import traceback

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
            # print server
            # traceback.print_exc()
    if len(ipList)>limit:
        with open('domain.log','a+') as f:
            line = '{}\tCDN\t{}'.format(site,','.join(ipList))
            f.write(line + '\n')
            print line
    elif 0<len(ipList)<=limit:
        with open('domain.log','a+') as f:
            line = '{}\tnoCDN\t{}'.format(site,','.join(ipList))
            f.write(line + '\n')
            print line
        with open('realIP.txt','a+') as f:
            for ip in ipList:
                if isIP(ip) and ip.strip() not in limitIP:
                    f.write(ip.strip()+'\n')
                    limitIP.append(ip.strip())
    else:
        with open('domain.log','a+') as f:
            line = site + '\t' + 'error'
            f.write(line + '\n')
            print line

if __name__ == '__main__':
    open('domain.log','a+').truncate()
    open('realIP.txt', 'a+').truncate()
    if os.path.isfile(sys.argv[1]):
        for line in open(sys.argv[1],'r+').readlines():
            dnsQuery(line.strip())
    else:
        dnsQuery(sys.argv[1].strip())

