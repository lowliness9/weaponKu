# -*- coding:utf-8 -*-
import requests
import re
import sys
from time import sleep
reload(sys)
sys.setdefaultencoding('utf-8')

def getVersion():
    try:
        request = requests.get(url='http://www.1234i.com/',headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Connection':'close',
        },timeout=8)
        if re.findall('name="ok2" value="(.+?)">',request.text):
            return re.findall('name="ok2" value="(.+?)">',request.text)[0]
    except:
        return False

def run(queryData):
    data = 'ok2={}&str={}&ipk=b&Submit=%C5%FA%C1%BF%B2%E9IP'.format(version,queryData)
    request = requests.post(url='http://www.1234i.com',headers = {
        'Origin':'http://www.1234i.com',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Accept':'*/*',
        'Referer':'http://www.1234i.com/',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'close'
    },timeout=8,data=data)
    request.encoding = 'utf-8'
    html = request.content
    var = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.+?<br>',html)
    if var:
        for v in var:
            retVal = v.replace('#<font color=blue>','\t').replace('</font>','\t').replace('<br>','')
            # print retVal
            with open('output.txt','a+') as f:
                f.write(retVal.strip()+'\n')
if __name__ == '__main__':
    version = getVersion()
    print 'Ver: {}'.format(version)
    tmpList = open(sys.argv[1],'r+').readlines()
    ipsList = [ip.strip() for ip in tmpList]
    count = len(ipsList)
    print 'IP: {}'.format(count)
    if count//300 >= 1:
        for i in range(0,count//300):
            li = ipsList[300*i:300*(i+1)]
            print 'Query: {}'.format(len(li))
            queryData = '%0D%0A'.join(li)
            run(queryData)
            sleep(10)
        if count-count//300*300 > 0:
            li = ipsList[count//300*300:]
            print 'Query: {}'.format(len(li))
            queryData = '%0D%0A'.join(li)
            run(queryData)
    else:
        print 'Query: {}'.format(len(ipsList))
        queryData = '%0D%0A'.join(ipsList)
        run(queryData)