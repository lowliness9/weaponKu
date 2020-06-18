环境 python2.7
依赖 pip install -r requirement.txt

使用说明:
usage: python vMather.py --file file.txt

2020

Usage:
  -u TARGET    test a single target (e.g. www.example.com)
  --file FILE  load targets from targetFile (e.g. ip.txt)
  -t NUM       num of threads/concurrent, 5 by default
  -s NUM       timeout setting, 5s by default
  -h, --help   show this help message and exit

-u 功能没有
--file 指定一个文件

数量较少使用默认线程5，较多使用-t设置，例如: -t 100

文件内容支持如下：
http://example.com
http:/example.com/xx/xx/x
http://ip
http://ip:port
http://ip:port/xx/xx/x
8.8.8.8
8.8.8.8:8080

输出结果:
当前时间命名.txt

规则编写: 必须以\t分割,name开头 :为key和value的分隔符号 支持多个responseContent 规则以#开头会跳过此规则
name:规则名称	responseContent:xxxxx
name:规则名称	responseContent:xxxxx	responseContent:xxxxx
name:规则名称	responseContent:xxxxx	responseContent:xxxxx	responseContent:xxxxx

例子:
name:svchost.exe	responseContent:svchost.exe
name:coinhiveJS挖矿	responseContent:coinhive.min.js	responseContent:miner.start

