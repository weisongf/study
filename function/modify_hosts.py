#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import os
import json
import paramiko
import traceback
import shutil

import time

import ConfigParser
import logging
import logging.handlers

LOG_FILE = '/tmp/rod_openstack_deploy.log'
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
#
with open("/opt/config/body.json", 'r+') as load_f:
    params = json.load(load_f)
    logger.info("Beginning load body json info:%s",params)
#config
RODS_CONF = "/etc/rod_server/rods.conf"

def get_config(filename):
    config = ConfigParser.ConfigParser()
    config.read(filename)

    return config

def remote_exec(ip, cmd):
    conf = get_config(RODS_CONF)
    ssh_user = conf.get('DEFAULT', 'ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    result = ''
    try:
        client.connect(hostname=ip, port=22, username=ssh_user, password=ssh_password)
        stdin, stdout, stderr = client.exec_command(cmd)
        result = stdout.readlines()
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


def env_hosts():
    #environid = params['environ']['environid']
    environid = "82"
    env_manageips_file = "/opt/config/env_manageips_" + environid
    hosts_manageip = []
    with open(env_manageips_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            hosts_manageip.append(line.split()[0])

    return   hosts_manageip

def modify_resolv(ip):

    cmd = 'grep role_type /opt/config/rc.ini |grep -E "compute|network|controller"'
    ops_cmd = '\cp -f /opt/config/hosts_openstack /etc/resolv.conf && echo "openstack_ok"'
    sto_cmd = '\cp -f /opt/config/hosts_ceph /etc/resolv.conf && echo "ceph_ok"'

    result = remote_exec(ip, cmd)
    print("The node:%s,role_type info:%s" % (ip, result))
    if result is not None:
        cmd_result = remote_exec(ip, ops_cmd)
    else:
        cmd_result = remote_exec(ip, sto_cmd)
    if cmd_result is not None:
        print("The node:%s,update resolv.conf:%s" % (ip, cmd_result))



#remote obtain files
def remote_getfile(ip,src_file,dst_file):
    conf = get_config(RODS_CONF)
    ssh_user = conf.get('DEFAULT', 'ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=ssh_user, password=ssh_password)
        client.connect(hostname=ip, port=22, username=ssh_user, password=ssh_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        logger.info("Beginning translate ceph conf files:%s", ip)

        sftp.get(src_file, dst_file)


    except Exception as e:
        logger.info('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
    finally:
        t.close()
        client.close()

#remote trans files
def remote_putfile(ip,dst_file,src_file):
    conf = get_config(RODS_CONF)
    ssh_user = conf.get('DEFAULT', 'ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=ssh_user, password=ssh_password)
        client.connect(hostname=ip, port=22, username=ssh_user, password=ssh_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        logger.info("Beginning translate ceph conf files:%s", ip)
        sftp.put(dst_file,src_file )

    except Exception as e:
        logger.info('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
    finally:
        t.close()
        client.close()



#remote obtain files
def remote_file(ip,method,src_file,dst_file):
    conf = get_config(RODS_CONF)
    ssh_user = conf.get('DEFAULT', 'ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=ssh_user, password=ssh_password)
        client.connect(hostname=ip, port=22, username=ssh_user, password=ssh_password)
        sftp = paramiko.SFTPClient.from_transport(t)

        if method == "get":
            logger.info("Beginning get ceph conf files to master node:%s", ip)
            sftp.get(src_file, dst_file)
        elif method == "put":
            logger.info("Beginning translate ceph conf files:%s", ip)
            sftp.put(dst_file, src_file)

    except Exception as e:
        logger.info('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
    finally:
        t.close()
        client.close()

# obtain ceph files
def ceph_conf(env_file):

    conf = get_config(env_file)
    ceph_manageips = conf.get('DEFAULT', 'ceph_manageips')
    ceph_deployip = ceph_manageips.split(',')[0]
    cmd = "cd /etc/;tar czf ceph.tar.gz ceph/"
    if ceph_deployip is not None:
        cmd_result = remote_exec(ceph_deployip, cmd)
    else:
        print("The ceph deploy node is null:%s", ceph_deployip)
    return ceph_deployip


def master_node_cephfile():
    env_file = "/opt/config/env_conf_file_82"
    ceph_deployip = ceph_conf(env_file)
    environid = "82"
    src_file = "/etc/ceph.tar.gz"
    dst_file = "/mnt/" + environid
    method = 'get'
    if os.path.exists(dst_file):
        logger.info("Dir exists:%s",dst_file)
    else:
        os.mkdir(dst_file)
    #remote_getfile(ceph_deployip, src_file, dst_file + "/ceph.tar.gz")
    remote_file(ceph_deployip, method,src_file, dst_file + "/ceph.tar.gz")

def add_node_cephfile(node_ip,environid):
    dst_file = "/mnt/" + environid + "/ceph.tar.gz"
    src_file = "/etc/ceph.tar.gz"
    cmd = "cd /etc/;tar xvf ceph.tar.gz"
    method = 'put'
    remote_file(node_ip, method,src_file,dst_file)
    remote_exec(node_ip, cmd)




def main():
    host_list = env_hosts()


    #for ip in host_list:
         #modify_resolv(ip)

    '''
    传输新增计算节点ceph配置文件
    1、把ceph deploy节点ceph配置文件放到server端
    2、把server端ceph配置文件传输到新增计算节点
    3、解压传输文件
   '''
    master_node_cephfile()

    node_ip = ["172.23.4.52"]
    environid = "82"

    for i in node_ip:
        add_node_cephfile(i, environid)


if __name__ == '__main__':
    main()



