# -*- coding: utf-8 -*-
import re
import sys
import requests
import threading
import time
requests.packages.urllib3.disable_warnings()

class WebSpider():

	def __init__(self,url):
		self.url = url
		# 过滤器关键字
		self.filter = [
			'.css','.js', '.jpg', 'png', '.html', '.gif', '#content',
			'javascript', 'style=', 'JavaScript','base64','<%', '.ico', '"','\'',
			'apple.com','opera.com','operachina.com','microsoft.com','google.com','mozillaonline.com','gov.cn',
			'cloudflare.com','51.la','qq.com','csdn.com','aliyun.com',
		]
		# 初始化self.TMPDB
		self.TMPDB = list()
		# 初始化self.resultDB
		self.resultDB = list()
		self.rootUrl = ''
		self.baseUrl = ''
		#初始化线程lock
		self.lock = threading.Lock()
		#单个网站采集url最大数量
		self.maxCount = 100
		#实时输出采集到的url
		self.log = True
		#是否需要输出结果
		self.outres = True
		#单个爬取时间
		self.timeMaxUse = 600
		#开始时间
		self.timestart = 0



	def getlinks(self,html):
		linkdb = []
		regex = re.compile("href=\"(.+?)\"")
		linkdb.extend(regex.findall(html))
		regex = re.compile("href=\'(.+?)\'")
		linkdb.extend(regex.findall(html))
		regex = re.compile("src=\'(.+?)\'")
		linkdb.extend(regex.findall(html))
		regex = re.compile("src=\"(.+?)\"")
		linkdb.extend(regex.findall(html))
		regex = re.compile("action=\'(.+?)\'")
		linkdb.extend(regex.findall(html))
		regex = re.compile("action=\"(.+?)\"")
		linkdb.extend(regex.findall(html))
		return linkdb

	def deallink(self,link):
		link = str(link).strip().replace('\\', '')
		link = link.split('://')[0] + '://' + re.sub('(\./)+', '/', link.split('://')[1])
		link = link.split('://')[0] + '://' + re.sub('/+', '/', link.split('://')[1])
		return link

	def printmsg(self,msg):
		print '{} [{}] {}'.format(time.strftime("[%H:%M:%S]", time.localtime()),len(self.resultDB),msg)

	def update(self,url):
		if url.endswith('/'):
			self.baseUrl = url
		else:
			self.baseUrl = url.replace(url.split('/')[-1], '')
		self.rootUrl = url.split('/')[0] + '//' + url.split('/')[2] + '/'

	def parselink(self,linkdb):
		for link in linkdb:
			ct = False
			for f in self.filter:
				if f in link:
					ct = True
					break
			if ct:
				continue
			if link in self.filter:
				continue

			if 'http' in link:
				self.TMPDB.append(link)
				# self.printmsg("found {}".format(link))
			else:
				if str(link).startswith('/'):
					self.TMPDB.append(self.rootUrl + link.strip('/'))
					# self.printmsg("found {}".format(self.rootUrl + link.strip('/')))
				else:
					self.TMPDB.append(self.baseUrl + link)
					# self.printmsg("found {}".format(self.baseUrl + link))


	def spider(self,url):
		self.TMPDB.append(url + '/')
		self.timestart = time.time()
		while True:
			if len(self.TMPDB) > 0 and len(self.resultDB) < self.maxCount and time.time() - self.timestart < self.timeMaxUse:
				url = self.TMPDB[0]
				if url in self.resultDB:
					self.TMPDB.remove(url)
					continue
				self.resultDB.append(url)
				self.TMPDB.remove(url)
				self.update(url)


				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
					'Connection': 'Keep-Alive'
				}
				try:
					self.printmsg("request {}".format(url))
					p = requests.get(url=url, headers=headers, timeout=8, allow_redirects=False, verify=False)
					# 解决302重定向问题
					if 300 < p.status_code and p.status_code < 400:
						if 'http' in p.headers['Location']:
							self.TMPDB.append(p.headers['Location'])
						else:
							self.TMPDB.append(self.rootUrl + p.headers['Location'].strip('/'))
						self.TMPDB = list(set(self.TMPDB))
						continue
					if p.status_code == 404:
						continue
					html = p.content
					linkdb = self.getlinks(html)

					# 抓取的链接数据处理
					self.parselink(linkdb)
					self.TMPDB = list(set(self.TMPDB))
				except Exception as e:
					self.TMPDB = list(set(self.TMPDB))
			else:
				break
			time.sleep(2)

		if self.outres:self.output()

	def output(self):
		with open('trb.txt','a+') as f:
			for u in self.resultDB:
				f.write(u.strip())

	def run(self):
		self.spider(self.url)

if __name__ == '__main__':
	url = sys.argv[1]
	spider = WebSpider(url)
	spider.run()
