#!/bin/bash

workDIR="/var/log/proxyLog"

name=$(date| awk '{print $4"-"$5}' | sed 's/:/-/g')

# GET SOCKS PROXY
proxybroker find --type SOCKS5 SOCKS4 -l 100 --outfile ${workDIR}/$name.sock.log

# SOCKS
cat ${workDIR}/$name.sock.log | grep sock -i | grep ", "  |  awk '{print $4,$6}'  | tr 'A-Z' 'a-z' | sed 's/\[//' | sed 's/,//' | sed 's/:/ /' | sed 's/>//' | sort > ${workDIR}/$name.proxy.log

# SOCKS
cat ${workDIR}/$name.sock.log | grep sock -i | grep ", " -v |  awk '{print $4,$5}'  | tr 'A-Z' 'a-z' | sed 's/\[//' | sed 's/,//' | sed 's/:/ /' | sed 's/>//' | sed 's/\]//' | sort >> ${workDIR}/$name.proxy.log

# GET HTTP PROXY
proxybroker find --type HTTP -l 100 --outfile ${workDIR}/$name.http.log

# HTTP
cat ${workDIR}/$name.http.log | grep HTTP -i | awk '{print $4,$6}'  | tr 'A-Z' 'a-z' | sed 's/\[//' | sed 's/,//' | sed 's/:/ /g' | sed 's/>//' | sed 's/\]//' | sort >> ${workDIR}/$name.proxy.log

rm -rf ${workDIR}/$name.sock.log 

rm -rf ${workDIR}/$name.http.log

dynamicProxy ${workDIR} $name.proxy.log

cat /etc/proxychains4.conf.base > /etc/proxychains4.conf.tmp

cat ${workDIR}/$(date +%Y-%m-%d-proxy.txt) >> /etc/proxychains4.conf.tmp

cat /etc/proxychains4.conf.tmp > /etc/proxychains4.conf

rm -rf /etc/proxychains4.conf.tmp

