#! /usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import os
import sys
import json
import subprocess
import traceback
import paramiko
import time
import ConfigParser
import re
import logging
import logging.handlers

LOG_FILE = '/var/log/rod_openstack_deploy.log'
# 实例化handler
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 512*512, backupCount = 5)
# 定义日志格式
fmt = '%(asctime)s %(process)d %(levelname)s %(filename)s:%(lineno)s %(name)s %(message)s'
# 实例化formatter
formatter = logging.Formatter(fmt)
# 为handler添加formatter
handler.setFormatter(formatter)
# 获取名为rod_server的logger
logger = logging.getLogger('rod_server')
# 为logger添加handler
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


with open("/opt/config/body.json", 'r+') as load_f:
    params = json.load(load_f)
    logger.info("Beginning load body json info:%s",params)

#读取配置文件信息
RODS_CONF = "/etc/rod_server/rods.conf"

def get_config():
    config = ConfigParser.ConfigParser()
    config.read(RODS_CONF)

    return config
# 全局属性
openstack_version = openstack_ver = params['environ']['openstack_version'].lower()
#remote执行命令
def remote_exec(ip,cmd):
    conf = get_config()
    ssh_user = conf.get('DEFAULT', 'ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    result = 'No nodes available'
    try:
        client.connect(hostname=ip, port=22, username=ssh_user, password=ssh_password)
        stdin, stdout, stderr = client.exec_command(cmd)
        result = stdout.readlines()
        print ip,result
        logger.info("CMD:%s exec result %s", cmd, result)
        client.close()
    except Exception as e:
        logger.info('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            logger.info("CMD failure")
    return result

def main():
    cmd ="ls  /root/nic_bak"
    for node in params['environ']['nodes']:
        for nic in node['nicbond']:
            if nic['netflag'] == 'admin':
                manage_ip = nic['ip']
        remote_exec(manage_ip, cmd)


if __name__ == '__main__':
    main()