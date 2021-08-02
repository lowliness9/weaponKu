#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project = https://github.com/lowliness9/pytools.git
# author = lowliness9
# date: 2020-04-21
from concurrent.futures import ThreadPoolExecutor
import threading
import requests
import sys
import argparse
import time


requests.packages.urllib3.disable_warnings()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Connection':'close'
}

args = dict()

sList = []

outputNamer = time.strftime("out_%m_%d_%H%M%S.txt", time.localtime())

def cmdLineParser():
    parser = argparse.ArgumentParser(description='proxyGoo verify that the agent can access google.com',
                                     usage='proxyGoo -file ip.txt',
                                     add_help=False)

    useage = parser.add_argument_group('Usage')

    useage.add_argument('-file', metavar='file', dest="targetFile", type=str, default='',
                        help='Load targets from targetFile (e.g. ip.txt format: 127.0.0.1:1080)')
    useage.add_argument('-t', metavar='num', dest="threadNum", type=int, default=30,
                        help='num of threads/concurrent, 30 by default')
    useage.add_argument('-type', metavar='http', dest="type", type=str, default='socks5',
                        help='Proxy type,socks5 default (e.g https,http,socks5)')
    useage.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args.update(vars(parser.parse_args()))


def output(content):
    lock.acquire()
    with open(outputNamer,'a+') as f:
        f.write(content+'\n')
    lock.release()

def sockConnect(address):
    address = address.strip()
    lock.acquire()
    print('\r [{}] {} #'.format(len(sList)-sList.index(address),address),end='')
    lock.release()

    proxies = {"http": "{}".format(address), "https": "{}".format(address)}
    try:
        request = requests.get('https://www.google.com/', proxies=proxies,timeout=(5,3),verify=False,headers=headers)
        # print(request.text)
        if request.status_code == 200 and '<title>Google</title>' in request.text:
            print('\r [+] Found {} #'.format(address))
            output(address)
    except:
        pass
        # traceback.print_exc(file=open('error.log','a+'))

def Builder():
    ipList = open(args['targetFile'],'r+').readlines()
    protocols = args['type'].split(',')
    for protocol in protocols:
        for ip in ipList:
            sList.append('{}://{}'.format(protocol.strip(),ip.strip()))

if __name__ == '__main__':
    cmdLineParser()
    Builder()
    print('[+]',len(sList))
    lock = threading.Lock()
    with ThreadPoolExecutor(args['threadNum']) as executor:
        executor.map(sockConnect,sList)















