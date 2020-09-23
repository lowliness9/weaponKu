# -*- coding:utf-8 -*-
import whois
from time import sleep as s
import traceback
open('output.txt','w').truncate()
with open('output.txt','a+') as f:
    for domain in open('input.txt', 'r+').readlines():
        domain = domain.strip()
        if domain:
            try:
                data = whois.whois(domain)
                print('--------------------------------------------------------------->')
                print('Domain: ',data['domain_name'])
                print('Registrar: ',data['registrar'])
                print('Email: ',data['emails'])
                print('--------------------------------------------------------------->')
                domain = data['domain_name'] if isinstance(data['domain_name'],(str)) else ','.join(data['domain_name'])
                registrar = data['registrar'] if isinstance(data['registrar'],(str)) else ','.join(data['registrar'])
                email = data['emails'] if isinstance(data['emails'],(str)) else ','.join(data['emails'])
                f.write('Domain: ' + domain + '\n')
                f.write('Registrar: ' + registrar + '\n')
                f.write('Email: ' + email + '\n')
                f.write('\n')
            except:

                print('--------------------------------------------------------------->')
                print('Error: ',domain)
                print('--------------------------------------------------------------->')
        s(0.3)
