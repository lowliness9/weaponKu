#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header

receiver = 'xxx@qq.com'
server = 'smtp.qq.com'
sender = 'xxx@qq.com'
username = sender
password = 'xxxxxxxx'


def mailSender(content):


    message = MIMEText(content, 'html', 'utf-8')
    # 发送者 接收者
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(receiver, 'utf-8')
    # 邮件主题
    message['Subject'] = Header('消息提醒!', 'utf-8')
    client = smtplib.SMTP_SSL(server)
    client.login(username, password)
    client.sendmail(sender,receiver, message.as_string())


mailSender(sys.argv[1].strip())
