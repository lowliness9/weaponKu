# proxyScan3
功能
---
`proxyScan3.py` 批量验证代理是否可以正常使用。

使用说明
---

proxyScan3 verify that the agent can access google.com  

Usage:  
* --file file  Load targets from targetFile (e.g. ip.txt format: 127.0.0.1:1080)  
* --t num      num of threads/concurrent, 30 by default  
* --type http  Proxy type,https default (e.g https or https,http,socks5)  
* -h, --help   show this help message and exit  
