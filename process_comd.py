#!/usr/bin/env python
#coding:utf-8
import threading
from multiprocessing import Pool
import paramiko
import time
import sys
 
while True:
    try:
        time.sleep(3)
        comd = raw_input('��������Ҫ�����ַ�������(����1�����ļ�)��')
    except:    
        sys.exit()
    else:
        #�Ĺ�����Ϊexit���˳�ϵͳ
        if comd == 'exit':
            sys.exit()
        
        #�������Ϊ1�ͽ��н���
        if comd == '1':
            try:
                yuan = raw_input('��������Դ�������ļ��ļ���·������/opt/test.txt��')
                mb = raw_input('��������Ŀ�����������ļ���·������/opt/test1.txt��')
            except:
                sys.exit()
        #��־�ļ�
        succ = '/opt/log.txt'
        err = '/opt/error.txt'
        def run(n):
            #����Key��·��
            private_key_path = '/root/.ssh/id_rsa'
            #���key
            key = paramiko.RSAKey.from_private_key_file(private_key_path)
            #��ȡ����ssh����
            ssh = paramiko.SSHClient()
            #�������Ӳ���know_hosts�ļ��е�����
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #�Ѿֲ�������Ϊȫ�ֱ���
            global yuan
            global mb
            #���ֵ����1�ʹ����ļ�
            if comd == '1':
                #��̨������IP��ַ
                ip='192.168.200.%s' %n
                t = paramiko.Transport((ip,22))
                t.connect(username='root',pkey=key)
                sftp = paramiko.SFTPClient.from_transport(t)
                result = sftp.put(yuan,mb)
                return result
                t.close()
                
            else:
                #��̨������IP��ַ
                ip='192.168.200.%s' %n
                ##���������Ϣ
                ssh.connect(hostname=ip, port=22, username='root', pkey=key)
                #ִ������
                stdin, stdout, stderr = ssh.exec_command(comd)
                #��ȡִ�������ʱ��
                sj = time.strftime('%Y-%m-%d %H:%M:%S')
                #����ȷ�ʹ�����־�ļ�
                f = open(succ,'ab')
                e = open(err,'ab')
                #������ȷ�ʹ�����Ϣ
                result_out = stdout.read()
                result_err = stderr.read()
                #����ȷ�ʹ�����Ϣд����־�ļ�
                if result_err:
                    e.write(sj+'\n')
                    e.write(result_err+'\n')
                    e.close
                else:
                    f.write(sj+'\n')
                    f.write(result_out+'\n')
                    f.close
                #�����ȷ�ʹ�����Ϣ
                return result_out
                return result_err
                #�ر�ssh����
                ssh.close();
        #���ͬʱִ�еĽ�����Ϊ3
        pool = Pool(processes=3)
        #����һ�����б�
        res_list = []
        #������������
        if __name__ == '__main__':
            for i in range(10,13):
                res = pool.apply_async(run, [i,])
                #�����б�����ֵ
                res_list.append(res)
            #���������
            for r in res_list:
                print r.get()