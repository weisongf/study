#! /usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import time
import os
import re

target_file = '/var/log/rod/host-192-168-56-11-rod-deploy.log'
init_flag = True  # 初次加载程序
time_kick = 5

record_count = 0

while True:
    print '当前读到了', record_count
    #没有日志文件，等待
    if not os.path.exists(target_file):
        print 'target_file not exist'
        time.sleep(time_kick)
        continue

    try:
        ip  = '192.168.56.11'
        easytime = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        file_name = '%s_user_%s.log' % (ip,easytime)
        f_w = open(file_name, 'w')
        if init_flag:
            #读取整个文件
            for eachline in fileinput.input(target_file):
                print eachline
                if re.search("完成部署ceph集群",eachline):
                    print("Deploy ceph successfully")
                else:
                    print("Deploy ceph no finish")
                f_w.write(eachline)
                record_count += 1

            init_flag = False
        else:
            #如果总行数小于当前行，那么认为文件更新了，从第一行开始读。
            total_count = os.popen('wc -l %s' % target_file).read().split()[0]
            total_count = int(total_count)
            if total_count < record_count:
                record_count = 0

            for eachline in fileinput.input(target_file):
                line_no = fileinput.filelineno()
                if line_no > record_count:
                    print eachline
                    f_w.write(eachline)
                    record_count += 1

        f_w.close()
    except:
        pass
    time.sleep(time_kick)