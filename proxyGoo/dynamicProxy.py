#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project = https://github.com/lowliness9/pytools.git
# author = lowliness9
# date: 2021-04-23
from concurrent.futures import ThreadPoolExecutor
import threading
import requests
import sys
import time
import os

requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Connection':'close'
}

workDIR = sys.argv[1]

lock = threading.Lock()

todayFlag = time.strftime("%Y-%m-%d-", time.localtime())

aliveProxyList = []

def outputAliveProxy(proxy):
    lock.acquire()
    print(proxy)
    with open(os.path.join(workDIR,todayFlag + 'proxy.txt'),'a+') as f:
        if proxy not in aliveProxyList:
            f.write(proxy.strip()+'\n')
    lock.release()

def ProxyTest(proxyList):
    procotol = proxyList[0]
    IP = proxyList[1]
    PORT = proxyList[2]

    proxies = {"http": "{}://{}:{}".format(procotol,IP,PORT), "https": "{}://{}:{}".format(procotol,IP,PORT)}
    try:
        request = requests.get(url = 'http://icanhazip.com/', proxies = proxies,timeout = (5,3) , verify = False,headers = headers)
        if request.text.strip() == IP:
            lock.acquire()
            print(' '.join(proxyList))
            lock.release()
            aliveProxyList.append(' '.join(proxyList))
    except:
        pass

def todayProxyTest(proxyList):
    procotol = proxyList[0]
    IP = proxyList[1]
    PORT = proxyList[2]

    proxies = {"http": "{}://{}:{}".format(procotol,IP,PORT), "https": "{}://{}:{}".format(procotol,IP,PORT)}
    try:
        request = requests.get(url = 'http://icanhazip.com/', proxies = proxies,timeout = (5,3) , verify = False,headers = headers)
        if request.text.strip() == IP:
            outputAliveProxy(' '.join(proxyList))
    except:
        pass

def Builder():
    proxyList = []
    proxyfileList = open(os.path.join(workDIR,sys.argv[2]),'r+').readlines()
    for proxy in proxyfileList:
        sinProxy = proxy.split()
        if sinProxy:proxyList.append(sinProxy)
    return proxyList


def checkHistory():
    if not os.path.exists(os.path.join(workDIR,todayFlag + 'proxy.txt')):
        with open(os.path.join(workDIR,todayFlag + 'proxy.txt'),'a+') as f:
            for proxy in aliveProxyList:
                if proxy:
                    f.write(proxy+'\n')
        os.remove(os.path.join(workDIR, sys.argv[2]))
    else:
        todayProxyList = []
        for proxy in open(os.path.join(workDIR,todayFlag + 'proxy.txt'),'r+').readlines():
            proxyT = proxy.strip().split()
            if proxyT:todayProxyList.append(proxyT)
        os.remove(os.path.join(workDIR,todayFlag + 'proxy.txt'))
        with ThreadPoolExecutor(20) as executor:
            executor.map(todayProxyTest,todayProxyList)
        for proxy in aliveProxyList:
            with open(os.path.join(workDIR, todayFlag + 'proxy.txt'), 'a+') as f:
                f.write(proxy.strip() + '\n')
        os.remove(os.path.join(workDIR,sys.argv[2]))

if __name__ == '__main__':

    proxyList = Builder()
    with ThreadPoolExecutor(20) as executor:
        executor.map(ProxyTest,proxyList)
    checkHistory()










