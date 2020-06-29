#!/usr/bin/python3

import requests
import re
import math
import time
import sys
import base64
from urllib.request import quote


# 获取页数
def page(url, headers):
    # 获取查询网页的源码
    url = "https://fofa.so/result?qbase64=" + url
    r = requests.get(url, headers=headers).text

    # print(r.encoding) # 查看当前网页编码
    # print(r.text)   # 查看网页源码

    # 正则规则
    g = 'id="total_entries" value="(.*?)" />'

    # 获取查询总数
    allnum = re.findall(g, r)

    # 将列表转换为整型
    allnum = int(allnum[0])

    # 输出总数量
    # print(allnum)

    # 利用函数向上取整，获得页数
    page = math.ceil(allnum / 10)

    # 输出提示信息
    print("一共查询到{}条信息，一共{}页。".format(allnum, page))

    return page


def sear_for(headers, page, arg):
    # 所有的页数链接
    url_list = []


    for i in range(1, page + 1):
        url = "https://fofa.so/result?qbase64=" + arg + "&page=" + str(i)
        "https://fofa.so/result?qbase64=cmVnaW9uPSJHdWFuZ2RvbmciICYmIHBvcnQ9IjcwMDEiJiZwcm90b2NvbD09IndlYmxvZ2ljIg%3D%3D&page=2"
        # 获取所有页数链接
        url_list.append(url)

        # 获取当前页面源码
        r = requests.get(url, headers=headers).text
        # 编写正则规则
        # g = '>(.*?) <i class="fa fa-link"></i></a>'

        # g = '<a target="_blank" href=".*?">(.*?)</a>'
        g = '>(.*?) <i class="fa fa-link"></i></a>'
        # 筛选出当前页面ip和端口
        ip = re.findall(g, r)

        # 输出提示信息
        print("[*] 当前已爬取第{}页的信息，共{}条。分别为{}".format(i, len(ip), ip))
        for j in range(len(ip)):

           write_file(ip[j])
        # 每隔5秒查询下一页，反反爬虫机制
        time.sleep(5)





def write_file(url):
    name = "fofa.so.txt"
    with open(name, 'a+',encoding='utf-8')as f:
            f.write(url+"\n")
    with open(name, 'r',encoding='utf-8')as f:
        lines = len(f.readlines())
        print('[*] {}共写入{}条数据'.format(name,lines))


if __name__ == '__main__':
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
               "Cookie": "_fofapro_ars_session=db46e884fc7b531824c163983259b168; Hm_lvt_9490413c5eebdadf757c2be2c816aedf=1592880242,1592880307; referer_url=%2Fresult%3Fqbase64%3DYXBwPSJEaWdpLUNvbm5lY3QtTUUi; Hm_lpvt_9490413c5eebdadf757c2be2c816aedf=1592880336"
               }

    try:

        # arg = str(sys.argv[1])
        arg = str(input("[*] 请输入要查询的信息："))

        arg = base64.b64encode(arg.encode('utf-8')).decode()
        arg = quote(arg)

        # 获取页数
        page = page(arg, headers)

        # 查询
        sear_for(headers, page, arg)



    except:
        pass
