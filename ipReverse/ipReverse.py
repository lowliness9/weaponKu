# -*- coding:utf-8 -*-
import socket
import re
import requests
from time import sleep as s

headers = {

    'x-apikey': '92a7a411239c5e401bc077f87c30c4653084a56425451d5b06c0705e22c7d199'

}

def isIPAddress(addr):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(addr):
        return True
    p = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}')
    if p.match(addr):
        return True
    else:
        return False

def telnetNu00(input):
    input = input.strip()
    if isIPAddress(input):input='ip:'+input
    try:
        sock = socket.socket()
        sock.connect(('nu00.com',23))
        sock.send(bytes('{}\n'.format(input),encoding='utf-8'))
        data = sock.recv(2048)
        data = str(data,encoding='utf-8')
        data = data.split('\r\n')
        with open('output.txt', 'a+') as f:
            for line in data:
                p = re.compile('((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)')
                if p.findall(line):
                    print(line)
                    # f.write("nu00\t"+ line+'\n')
                    f.write(line.split(' ')[0]+"\t"+line.split(" ")[1]+"\n")
    except:
        pass


def func_nu00com():
    open('output.txt', 'w').truncate()
    for addr in open('input.txt','r+').readlines():
        addr = addr.strip()
        if addr:
            telnetNu00(addr)
        s(0.3)

def func_vt():
    ipObj = open('input.txt', 'r+').readlines()
    url = \
        'https://www.virustotal.com/api/v3/ip_addresses/{}/resolutions?limit=40'
    for queryIP in ipObj:
        queryIP = queryIP.strip()
        if queryIP and isIPAddress(queryIP):
            try:
                request = requests.get(url.format(queryIP), headers=headers)
                resolution = request.json()['data']
                ct = len(resolution)
                with open('output.txt','a+') as f:
                    for attr in resolution:
                        data = attr['attributes']['ip_address'] + "\t" + attr['attributes']['host_name']
                        print(data)
                        f.write(data+"\n")
            except:
                pass
                # print(queryIP + '\t' + '0\t' + 'Error')
        s(0.3)

if __name__ == '__main__':
    func_nu00com()
    func_vt()

