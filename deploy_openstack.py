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

def get_conf(filename):
    config = ConfigParser.ConfigParser()
    config.read(filename)

    return config

def update_conf(filename):
    config = ConfigParser.ConfigParser()
    config.write(filename)

    return config
# 全局属性
openstack_version = openstack_ver = params['environ']['openstack_version'].lower()
# 定义生成主机hosts文件函数
def hosts_create(params):
    environid = params['environ']['environid']
    nodes_list = params['environ']['nodes']
    controller_internal_vip = nodes_list[0]['intervip']
    hosts_ops_file = "/opt/config/hosts_openstack_" + environid
    hosts_ceph_file = "/opt/config/hosts_ceph_" + environid
    ha_enable = params['environ']['haenabled']
    hosts_openstack_inter = {}
    hosts_openstack_stor = {}
    hosts_manageip = {}
    hosts_ceph = {}
    for hosts_num in range(0, len(nodes_list), 1):
        hostname = nodes_list[hosts_num]['hostname']
        for nics_num in range(0, len(nodes_list[hosts_num]['nicbond']), 1):
            if 'admin' == nodes_list[hosts_num]['nicbond'][nics_num]['netflag']:
                hosts_manageip[hostname] = nodes_list[hosts_num]['nicbond'][nics_num]['ip']
        if 'storage' not in nodes_list[hosts_num]['type'].split(","):
            for nics_num in range(0, len(nodes_list[hosts_num]['nicbond']), 1):
                if 'internaladmin' == nodes_list[hosts_num]['nicbond'][nics_num]['netflag']:
                    hosts_openstack_inter[hostname] = nodes_list[hosts_num]['nicbond'][nics_num]['ip']
                if 'storage' == nodes_list[hosts_num]['nicbond'][nics_num]['netflag']:
                    hosts_openstack_stor[hostname] = nodes_list[hosts_num]['nicbond'][nics_num]['ip']
        else:
            for nics_num in range(0, len(nodes_list[hosts_num]['nicbond']), 1):
                if 'storage' == nodes_list[hosts_num]['nicbond'][nics_num]['netflag']:
                    hosts_ceph[hostname] = nodes_list[hosts_num]['nicbond'][nics_num]['ip']
    hosts_ops_all = dict(hosts_openstack_inter, **hosts_ceph)
    hosts_ceph_all = dict(hosts_openstack_stor, **hosts_ceph)
    logger.info("Hosts info alreay obtain hosts_ops_all:%s,hosts_ceph_all:%s", hosts_ops_all,hosts_ceph_all)
    if os.path.exists(hosts_ops_file):
        os.remove(hosts_ops_file)
    if os.path.exists(hosts_ceph_file):
        os.remove(hosts_ceph_file)

    with open(hosts_ceph_file, 'a') as f_ceph:
        f_ceph.write('127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4' + '\n' \
                                                                                                        '::1         localhost localhost.localdomain localhost6 localhost6.localdomain6' + '\n')
        for k in sorted(hosts_ceph_all):
            f_ceph.write(hosts_ceph_all[k] + ' ' + k + '\n')

    with open(hosts_ops_file, 'a') as f:
        f.write('127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4' + '\n' \
                                                                                                   '::1         localhost localhost.localdomain localhost6 localhost6.localdomain6' + '\n')
    if ha_enable:
        with open(hosts_ops_file, 'a') as f:
            f.write(controller_internal_vip + ' ' + 'controller' + '\n')
            for k in sorted(hosts_ops_all):
                f.write(hosts_ops_all[k] + ' ' + k + '\n')
    else:
        with open(hosts_ops_file, 'a') as f:
            for k in sorted(hosts_ops_all):
                f.write(hosts_ops_all[k] + ' ' + k + '\n')

    return hosts_manageip
# ceph info abtain
def ceph_info(params):
    nodes_list = params['environ']['nodes']
    ceph_members = []
    ceph_manageips = []
    ceph_mon_members = []
    ceph_osd_members = []
    nodes_len = len(params['environ']['nodes'])
    # 获取ceph配置信息
    for hosts_num in range(0, nodes_len, 1):
        enable_services = nodes_list[hosts_num]['component']
        if 'storage' in nodes_list[hosts_num]['type'].split(","):
            for nics_num in range(0, len(nodes_list[hosts_num]['nicbond']), 1):
                if 'storage' == nodes_list[hosts_num]['nicbond'][nics_num]['netflag']:
                    storage_ip = nodes_list[hosts_num]['nicbond'][nics_num]['ip']
                    ceph_members.append(storage_ip)
                    if 'ceph-mon' in enable_services.split(","):
                        ceph_mon_members.append(storage_ip)
                    if 'ceph-osd' in enable_services.split(","):
                        ceph_osd_members.append(storage_ip)
                elif  'admin' == nodes_list[hosts_num]['nicbond'][nics_num]['netflag']:
                    ceph_manageips.append(nodes_list[hosts_num]['nicbond'][nics_num]['ip'])
    ceph_deploy_ip = ceph_members[0]
    ceph_members = ",".join(ceph_members)
    ceph_mon_members = ",".join(ceph_mon_members)
    ceph_osd_members = ",".join(ceph_osd_members)
    return ceph_deploy_ip,ceph_members,ceph_mon_members,ceph_osd_members,ceph_manageips

# controller info obatin
def controller_info(params):
    controller_manage_members = []
    controller_internal_members = []

    for node in params['environ']['nodes']:
        if 'controller' in node['type'].split(","):
            for nic in node['nicbond']:
                if 'admin' == nic['netflag']:
                    manage_ip = nic['ip']
                    controller_manage_members.append(manage_ip)
                elif 'internaladmin' == nic['netflag']:
                    internal_ip = nic['ip']
                    controller_internal_members.append(internal_ip)
    controller_nums = len(controller_manage_members)
    upstream_manage_ip = controller_manage_members[0]
    upstream_internal_ip = controller_internal_members[0]
    controller_manage_members = ",".join(controller_manage_members)
    return  controller_nums,upstream_internal_ip,upstream_manage_ip,controller_manage_members,controller_internal_members

# 定义生成模板配置文件函数
def parser_dicts(params):
    conf = get_config()
    tem_path = conf.get('DEFAULT', 'j2_path')
    j2_path = os.path.abspath(tem_path)
    rc_path = '/opt/config'
    j2_env = Environment(loader=FileSystemLoader(j2_path))
    openstack_version = params['environ']['openstack_version']
    nodes_property = {'common': {}, 'nodes': {}}
    nodes_len = len(params['environ']['nodes'])
    # ceph配置信息
    logger.debug("Beginning to obtain ceph info")
    (ceph_deploy_ip, ceph_members, ceph_mon_members, ceph_osd_members, ceph_manageips) = ceph_info(params)
    logger.info("Obtaining ceph info ceph_deploy_ip:%s,ceph_members:%s,ceph_mon_members:%s,ceph_osd_members:%s",
                ceph_deploy_ip, ceph_members, ceph_mon_members, ceph_osd_members)
    # 获取HA参数配置信息
    (controller_nums, upstream_internal_ip, upstream_manage_ip, controller_manage_members,
     controller_internal_members) = controller_info(params)
    # Render openstack conf template
    nodes_property['common']['openstack_version'] = params['environ']['openstack_version']
    nodes_property['common']['netmode'] = params['environ']['netmode']
    nodes_property['common']['nettype'] = params['environ']['nettype']
    nodes_property['common']['bondmode'] = params['environ']['bondmode']
    nodes_property['common']['bondenabled'] = params['environ']['bondenabled']
    nodes_property['common']['haenabled'] = params['environ']['haenabled']
    for nodes_num in range(0, nodes_len, 1):
        nodes_property['nodes']['serverid'] = params['environ']['nodes'][nodes_num]['serverid']
        nodes_property['nodes']['hostname'] = params['environ']['nodes'][nodes_num]['hostname']
        nodes_property['nodes']['ntp_server_ip'] = params['environ']['nodes'][nodes_num]['ntp_server_ip']
        nodes_property['nodes']['type'] = params['environ']['nodes'][nodes_num]['type']
        nodes_property['nodes']['component'] = params['environ']['nodes'][nodes_num]['component']
        nodes_property['nodes']['managevip'] = params['environ']['nodes'][nodes_num]['managevip']
        nodes_property['nodes']['intervip'] = params['environ']['nodes'][nodes_num]['intervip']
        for nics_num in range(0, len(params['environ']['nodes'][nodes_num]['nicbond']), 1):
            if 'admin' == params['environ']['nodes'][nodes_num]['nicbond'][nics_num]['netflag']:
                nodes_property['nodes']['adminnet'] = params['environ']['nodes'][nodes_num]['nicbond'][nics_num]
            elif 'internaladmin' == params['environ']['nodes'][nodes_num]['nicbond'][nics_num]['netflag']:
                nodes_property['nodes']['internet'] = params['environ']['nodes'][nodes_num]['nicbond'][nics_num]
            elif 'business' == params['environ']['nodes'][nodes_num]['nicbond'][nics_num]['netflag']:
                nodes_property['nodes']['bussnet'] = params['environ']['nodes'][nodes_num]['nicbond'][nics_num]
            elif 'storage' == params['environ']['nodes'][nodes_num]['nicbond'][nics_num]['netflag']:
                nodes_property['nodes']['stornet'] = params['environ']['nodes'][nodes_num]['nicbond'][nics_num]
        # mitaka or ocata version
        logger.info("Beginning render host:%s,template", nodes_property['nodes']['adminnet']['ip'])
        with open(os.path.join(rc_path, "rc_" + nodes_property['nodes']['adminnet']['ip'] + ".ini"), 'w') as f:
            f.write(j2_env.get_template('rc_' + openstack_version.lower() + '.ini').render(
                nodes_property=nodes_property,
                upstream_internal_ip=upstream_internal_ip,
                upstream_manage_ip=upstream_manage_ip,
                ceph_deploy_ip=ceph_deploy_ip,
                ceph_members=ceph_members,
                ceph_mon_members=ceph_mon_members,
                ceph_osd_members=ceph_osd_members,
                controller_nums=controller_nums,
                controller_manage_members=controller_manage_members,
                controller_internal_members=controller_internal_members
            ))
        logger.info("End render host:%s,template", nodes_property['nodes']['adminnet']['ip'])
#调用shell命令
def execute_command(cmd):
    print('start executing cmd...')
    s = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stderrinfo, stdoutinfo = s.communicate()
    print('stderrinfo is -------> %s and stdoutinfo is -------> %s' % (stderrinfo, stdoutinfo))
    print('finish executing cmd....')
    return s.returncode
#delete known_hosts 匹配的行
def del_known(manageip):
    del_cmd = "sed -i '/^" + manageip + "/d' /root/.ssh/known_hosts"
    result = execute_command(del_cmd)
    return result

def del_exists_hosts():
    hosts_manageip = hosts_create(params)
    for v in hosts_manageip.values():
        del_known(v)
#准备部署脚本
def prepare_scripts_openstack_deployments(openstack_ver):
    cmd = ["cd /opt;tar" + " cvf " + openstack_ver + '_fly'+ ".tar" + " " + openstack_ver + '_fly'+ " " +  "common","cd /opt/config;tar cvf repos.tar repos"]
    for cmd_nums in range(0,len(cmd),1):
        result = execute_command(cmd[cmd_nums])
        print('result:------>', result)
    return result


#生成分发hosts文件信息并配置免密,借助ansible
def prepare_hosts(params):
    conf = get_config()
    ssh_user = conf.get('DEFAULT', 'ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    environid = params['environ']['environid']
    hosts_manageip_file = "/opt/config/hosts_manageips_" + environid
    hosts_manageip=hosts_create(params)
    if os.path.exists(hosts_manageip_file):
        os.remove(hosts_manageip_file)
    #生成管理网IP地址hosts信息
    with open(hosts_manageip_file, 'a') as f:
        f.write('[openstack]' + '\n')
        for v in hosts_manageip.values():
            f.write( v + ' ' + 'ansible_ssh_user=' + ssh_user + ' ansible_ssh_pass=' + ssh_password + ' ansible_ssh_port=22' + '\n')
    #cmd = "cp -a " +  hosts_manageip_file + " " + "/opt/ansible/hosts"
    #execute_command(cmd)
    anb_cmd = "cd /opt/ansible;ansible-playbook --inventory-file=" + hosts_manageip_file + " /opt/ansible/rsync_key.yml"
    keygen_cmd="ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa"
    #配置server节点和agent节点间免密
    if os.path.exists('/root/.ssh/id_rsa'):
        execute_command("rm -f /root/.ssh/*")
    result = execute_command(keygen_cmd)
    print('result:------>', result)
    result = execute_command(anb_cmd)
    print('result:------>', result)

#准备分发资源
# 主机hosts文件
# 渲染生成的模板文件
# tar包资源
def dispatch_res(params):
    environid = params['environ']['environid']
    openstack_version = params['environ']['openstack_version'].lower()
    dst_dir = '/opt/config'
    trans_files = [{'/opt/config/rc_': '/opt/config/rc.ini'},
                   {'/opt/config/hosts_ceph_' + environid: '/opt/config/hosts_ceph'},
                   {'/opt/config/hosts_openstack_' + environid: '/opt/config/hosts_openstack'},
                   {'/opt/' + openstack_version + '_fly.tar': '/opt/config/' + openstack_version + '_fly.tar'},
                   {'/opt/config/repos.tar': '/opt/config/repos.tar'}
                   ]
    conf = get_config()
    ssh_user = conf.get('DEFAULT', 'ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    hosts_manageip = hosts_create(params)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for v in hosts_manageip.values():
        try:
            t = paramiko.Transport((v, 22))
            t.connect(username=ssh_user, password=ssh_password)
            client.connect(hostname=v, port=22, username=ssh_user, password=ssh_password)
            sftp = paramiko.SFTPClient.from_transport(t)
            try:
                sftp.chdir(dst_dir)
            except IOError:
                sftp.mkdir(dst_dir)
            # 传输模板文件及hosts文件
            logger.info("Beginning translate deploy files")
            sftp.put(''.join(trans_files[0].keys()) + v + '.ini', ''.join(trans_files[0].values()))
            for i in range(1, len(trans_files), 1):
                for (key, values) in trans_files[i].items():
                    sftp.put(''.join(key), ''.join(values))
                    if ''.join(values)[-7:] == 'fly.tar':
                        stdin, stdout, stderr = client.exec_command('cd /opt/config;tar xvf ' + ''.join(
                            values) + ' > /dev/null 2>&1;rm -rf ../common;mv common ../;rm -rf ../*_fly;mv *_fly ../ ;chmod -R +x ../common ../*_fly')
                    elif ''.join(values)[-7:] == 'pos.tar':
                        stdin, stdout, stderr = client.exec_command(
                            'cd /opt/config;tar xvf ' + ''.join(values) + ' > /dev/null 2>&1')
        except Exception as e:
            logger.info('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
        finally:
            t.close()
            client.close()
#
def get_progress(remote_ip, cmd):
    conf = get_config()
    username = conf.get('DEFAULT', 'ssh_username')
    password = conf.get('DEFAULT', 'ssh_password')
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=remote_ip, port=22, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        progress = 'OpenStack deploying. \n' + stdout.read().decode('utf-8')
    except Exception as error:
        logger.exception('Caught exception: %s', error)
    finally:
        ssh_client.close()

    return progress

#获取信息
def get_node_deployment_progress(node_uuid):
    logger.debug("Get node %s deployment progress...", node_uuid)
    node_info = params['environ']['nodes']
    for node in node_info:
        if node_uuid == node.get("uuid"):
            for nic in node.get("nicbond"):
                if nic.get("netflag") == 'admin':
                    manage_ip = nic.get("ip")
    print("manage_ip:%s" % (manage_ip))
    conf = get_config()
    operation_log = conf.get('DEFAULT', 'operation_log')
    cmd = 'tail -n 1 ' + operation_log
    print("operation_log:%s" % (operation_log))
    progress = get_progress(manage_ip, cmd)  # Update to Done if getting keyword for success
    if 'StartServiceSuccess' in progress:
        progress = 'Done'

    return progress

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
        logger.info("%s,CMD:%s exec result %s",ip, cmd, result)
        client.close()
    except Exception as e:
        logger.info('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            logger.info("CMD failure")
    return result

#ssh exec shell
def ssh_exec(ip,cmd):
    conf = get_config()
    ssh_user = conf.get('DEFAULT','ssh_username')
    ssh_password = conf.get('DEFAULT', 'ssh_password')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    result = ''
    try:
        client.connect(hostname=ip, port=22,username=ssh_user,password=ssh_password)
        stdin, stdout, stderr = client.exec_command( cmd )
        result = stdout.readlines()
        #print stdout.readlines()
        client.close()
    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            print("CMD failure")
    return result

#check_install_log
def check_install(params):
    openstack_ver = params['environ']['openstack_version'].lower()
    exec_dir = "/opt/" + openstack_ver + "_fly"
    starservice_cmd = 'nohup sh ' + exec_dir + '/start_service.sh > /dev/null 2>&1 &'
    check_install_log = "grep InstallServiceSuccess /var/log/openstack/deploy.log"
    check_ceph_status = 'ceph health |grep -E "OK|WARN"'
    con_manip = []
    net_manip = []
    com_manip = []
    con_uuid = []
    net_uuid = []
    com_uuid = []
    # obtain all nodes role info
    for node in params['environ']['nodes']:
        role_type = node['type']
        node_uuid = node['uuid']
        for nic in node['nicbond']:
            if nic['netflag'] == 'admin':
                manage_ip = nic['ip']
        if 'controller' in role_type:
            con_manip.append(manage_ip)
            con_uuid.append(node_uuid)
        if 'network' in role_type:
            net_manip.append(manage_ip)
            net_uuid.append(node_uuid)
        if 'compute' in role_type:
            com_manip.append(manage_ip)
            com_uuid.append(node_uuid)
    # start controller node services
    for manip in con_manip:
        while True:
            con_status = True
            inst_result = remote_exec(manip, check_install_log)
            if inst_result:
                logger.info('controller node install packages successful:%s', manip)
                ceph_result = remote_exec(manip, check_ceph_status)
                logger.info('Ceph Health result:%s', ceph_result)
                if ceph_result:
                    remote_exec(manip, starservice_cmd)
                    break
                else:
                    con_status = False
                    time.sleep(10)
            else:
                time.sleep(10)
        if con_status:
            logger.info("Controller node already started services:%s", manip)
    logger.info("All Controller nodes already started services waiting 30s for network and compute")
    time.sleep(30)
    # controller nodes start services status value
    for uuid in con_uuid:
        while True:
            ser_result = get_node_deployment_progress(uuid)
            if ser_result == 'Done':
                logger.info("Controller node already started services successful:%s", uuid)
                break
            else:
                logger.info("Controller node already started services no successful continuing check:%s", uuid)
                time.sleep(10)
    logger.info("All Controller nodes already started services successful.")

    # start network services
    net_list = list(set(net_manip) - set(con_manip))

    if net_list:
        for net_node in net_list:
            while True:
                inst_result = remote_exec(net_node, check_install_log)
                if inst_result:
                    remote_exec(net_node, starservice_cmd)
                    logger.info('Network node install packages successfully and starting services:%s', net_node)
                    break
                else:
                    logger.info('network node packages installing:%s', net_node)
                    time.sleep(10)
    else:
        logger.info("Network nodes and Controller at the same  nodes ,services already start")

    # network nodes start services status value
    for uuid in net_uuid:
        while True:
            ser_result = get_node_deployment_progress(uuid)
            if ser_result == 'Done':
                logger.info("Network node already started services successful:%s", uuid)
                break
            else:
                logger.info("Network node already services no successful continuing check:%s", uuid)
                time.sleep(10)
    logger.info("All Network nodes already started services successful.")

    # start compute services
    com_list = list(set(com_manip) - set(net_manip))
    if com_list:
        for com_node in com_list:
            while True:
                inst_result = remote_exec(com_node, check_install_log)
                if inst_result:
                    remote_exec(com_node, starservice_cmd)
                    logger.info('Compute node packages install successfully and starting services:%s', com_node)
                    break
                else:
                    logger.info('Compute node packages installing:%s', com_node)
                    time.sleep(10)
    else:
        logger.info("Compute nodes and Network nodes at the same,services already start")
#check service log
def check_services(params):
    openstack_ver = params['environ']['openstack_version'].lower()
    exec_dir = "/opt/" + openstack_ver + "_fly"
    check_service_log = 'grep "StartServiceSuccess" /var/log/openstack/deploy.log'
    verify_servicecmd = 'nohup sh ' + exec_dir + '/verify.sh  > /dev/null 2>&1 &'

    #obtain controller nodes info include ha & no ha
    (con_nums, upstream_internal_ip, upstream_manage_ip, con_manage_members,con_internal_members) = controller_info(params)
    con_manip = list(con_manage_members.split(','))
    while True:
        all_status = True
        for node in params['environ']['nodes']:
            role_type = node['type']
            for nic in node['nicbond']:
                if nic['netflag'] == 'admin':
                    manage_ip = nic['ip']
            if 'controller'  in role_type or 'network'  in role_type or 'compute'  in role_type:
                ser_result = remote_exec(manage_ip, check_service_log)
                print(ser_result)
                if 'StartServiceSuccess' in ','.join(ser_result):
                    print("%s ,%s services start successful",role_type,manage_ip)
                else:
                    all_status = False
                    time.sleep(10)
                    break
        if all_status:
            print('All nodes services start successful')
            #start verify scripts
            remote_exec(con_manip[0], verify_servicecmd)
            logger.info("Controller node start verify service scripts")
            break
        else:
            time.sleep(10)
#check if VerifyServiceSuccess
def verify_services(params):
    check_verify_log = 'grep "VerifyServiceSuccess" /var/log/openstack/deploy.log '
    verify_file = 'cat /var/log/openstack/verify_result.log '
    (con_nums, upstream_internal_ip, upstream_manage_ip, con_manage_members,con_internal_members) = controller_info(params)
    con_manip = list(con_manage_members.split(','))
    while True:
        verify_result = remote_exec(con_manip[0], check_verify_log)
        if verify_result:
            logger.info("VerifyService execution is completed ")
            out_result = remote_exec(con_manip[0], verify_file)
            logger.info("The verity result info:%s",out_result)
            break
        else:
            logger.info("VerifyService execution is unfinished continuing ")
            time.sleep(10)
#触发执行new
def trigger_exec(params):
    openstack_ver = params['environ']['openstack_version'].lower()
    nodes_info = {}
    exec_dir = "/opt/" + openstack_ver + "_fly"
    (ceph_deploy_ip, ceph_members, ceph_mon_members, ceph_osd_members, ceph_manageips) = ceph_info(params)
    netcfg_cmd = 'nohup sh ' + exec_dir + '/prepare_env.sh > /dev/null 2>&1 &'
    start_cmd = 'nohup sh ' + exec_dir + '/deploy_openstack.sh > /dev/null 2>&1 &'
    check_netcfg = 'grep PrepareEnvSuccess /var/log/openstack/deploy.log'
    check_start = 'test -d /var/log/openstack && echo $?'
    # netconfig
    logger.info("Staring All nodes  net config")
    for node in params['environ']['nodes']:
        for nic in node['nicbond']:
            if nic['netflag'] == 'admin':
                manage_ip = nic['ip']
        time.sleep(2)
        remote_exec(manage_ip, netcfg_cmd)
        logger.info("node  net config:%s", manage_ip)
    # check netconfig
    while True:
        conf_status = True
        for node in params['environ']['nodes']:
            for nic in node['nicbond']:
                if nic['netflag'] == 'admin':
                    manage_ip = nic['ip']
            conf_result = remote_exec(manage_ip, check_netcfg)
            if conf_result:
                logger.info("%s  node net cfg success", manage_ip)
            else:
                conf_status = False
                logger.info("%s  nodes net cfg in progress", manage_ip)
                check_start_result = remote_exec(manage_ip, check_start)
                if check_start_result:
                    logger.info("%s  nodes net cfg scripts already execute", manage_ip)
                else:
                    remote_exec(manage_ip, netcfg_cmd)
        if conf_status:
            logger.info("All nodes net cfg success")
            break
        else:
            time.sleep(20)
    # start install
    logger.info("Staring All nodes  installing")
    remote_exec(ceph_manageips[0], start_cmd)
    #触发执行部署
    for nodes_num in range(0, len(params['environ']['nodes']), 1):
        nodes_info['role_type'] = params['environ']['nodes'][nodes_num]['type']
        for nics_num in range(0, len(params['environ']['nodes'][nodes_num]['nicbond']), 1):
            if 'admin' == params['environ']['nodes'][nodes_num]['nicbond'][nics_num]['netflag']:
                nodes_info['manageip'] = params['environ']['nodes'][nodes_num]['nicbond'][nics_num]['ip']
        if  ('controller' in  nodes_info['role_type'] or 'network' in  nodes_info['role_type'] or 'compute' in  nodes_info['role_type']) and nodes_info.get('manageip') != ceph_manageips[0]:
            remote_exec(nodes_info.get('manageip'), start_cmd)
    #检查安装进度并启动服务
    check_install(params)
    #check_services(params)
    #verify_services(params)

#清理安装log
def clean_nodeslog(params):
    cmd = "rm -rf /var/log/openstack/*.log"
    for node in params['environ']['nodes']:
        for nic in node['nicbond']:
            if nic['netflag'] == 'admin':
                manage_ip = nic['ip']
        log_result = ssh_exec(manage_ip, cmd)
        print("clean node:%s install log result:%s" %(manage_ip,log_result))

#清理节点安装包
def clean_nodespkg(params):
    con_pkg_cmd = ["rm -rf /var/log/openstack/*.log /etc/ceph/*;mkdir -p /root/bak_net;mv -f /etc/sysconfig/network-scripts/ifcfg-ens2* /root/bak_net;cp -f /root/nic_bak/* /etc/sysconfig/network-scripts/;nohup yum remove -y httpd keystone openstack-glance-* openstack-nova-* openstack-neutron-* openstack-cinder-* openstack-dashboard mariadb MySQL-python mariadb-server rabbitmq-server ceph net-tools pacemaker pcs corosync fence-agents resource-agents libqb0 haproxy openvswitch python-rbd python-rados librbd1 python-cephfs libcephfs1 librados2;rm -rf /var/lib/mysql /etc/my.cnf*;reboot > /dev/null 2>&1 &",
                   "rm -rf /var/log/openstack/*.log /etc/ceph/*;mkdir -p /root/bak_net;mv -f /etc/sysconfig/network-scripts/ifcfg-ens2* /root/bak_net;cp -f /root/nic_bak/* /etc/sysconfig/network-scripts/;nohup yum remove -y openstack-neutron-* openvswitch ceph mariadb MySQL-python mariadb-server net-tools pacemaker pcs corosync fence-agents resource-agents libqb0 haproxy python-rbd python-rados librbd1 python-cephfs libcephfs1 librados2;rm -rf /etc/openvswitch/*;rm -rf /etc/my.cnf*;reboot > /dev/null 2>&1 &",
                   "rm -rf /var/log/openstack/*.log /etc/ceph/*;mkdir -p /root/bak_net;mv -f /etc/sysconfig/network-scripts/ifcfg-ens2* /root/bak_net;cp -f /root/nic_bak/* /etc/sysconfig/network-scripts/;nohup yum remove -y openstack-neutron-* openstack-nova-* openvswitch libvirt ceph python-rbd python-rados librbd1 python-cephfs libcephfs1 librados2;rm -rf /etc/openvswitch/*;reboot > /dev/null 2>&1 &",
                   "rm -rf /var/log/openstack/*.log /etc/ceph/*;mkdir -p /root/bak_net;mv -f /etc/sysconfig/network-scripts/ifcfg-ens2* /root/bak_net;cp -f /root/nic_bak/* /etc/sysconfig/network-scripts/;nohup yum remove -y ceph ceph-common python-rbd python-rados librbd1 python-cephfs libcephfs1 librados2;systemctl stop ceph-osd@*;umount -a;rm -rf /var/lib/ceph;reboot > /dev/null 2>&1 &"
                   ]
    for node in params['environ']['nodes']:
        role_type = node['type']
        for nic in node['nicbond']:
            if nic['netflag'] == 'admin':
                manage_ip = nic['ip']
        if 'controller' in role_type:
            pkg_result = ssh_exec(manage_ip, con_pkg_cmd[0])
            print "clean nodes:%s" % (manage_ip)
            if pkg_result:
                print pkg_result
        elif  'network' in role_type:
            pkg_result = ssh_exec(manage_ip, con_pkg_cmd[1])
            print "clean nodes:%s" % (manage_ip)
            if pkg_result:
                print pkg_result
        elif  'compute' in role_type:
            pkg_result = ssh_exec(manage_ip, con_pkg_cmd[2])
            print "clean nodes:%s" % (manage_ip)
            if pkg_result:
                print pkg_result
        elif 'storage' in  role_type:
            pkg_result = ssh_exec(manage_ip, con_pkg_cmd[3])
            print "clean nodes:%s" % (manage_ip)
            if pkg_result:
                print pkg_result

#网络连通性检查
def netcheck(ip):
   try:
    p = subprocess.Popen(["ping -c 3 -W 1 "+ ip],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out=p.stdout.read()
    err=p.stderr.read()
    regex_out=re.compile('100% packet loss')
    regex_err=re.compile('unknown host')
    if len(regex_err.findall(err)) == 0:
        if len(regex_out.findall(out)) == 0:
            print ip + ': host up'
            return 'UP'
        else:
            print ip + ': host down'
            return 'DOWN'
    else:
        print ip + ': host unknown please check DNS'
   except:
       print 'NetCheck work error!'
   return 'ERR'

#检查所有节点网络连通性
def nodesconn(params):
    for node in params['environ']['nodes']:
        while True:
            for nic in node['nicbond']:
                if nic['netflag'] == 'admin':
                    manage_ip = nic['ip']
            net_result = netcheck(manage_ip)
            if net_result == 'UP':
                print("the node ping UP:%s" %(manage_ip))
                break
            else:
                print("the node ping Down & Err:%s" % (manage_ip))
                time.sleep(10)
    print("All nodes ping UP.")

def update_ini():
    ceph_deploy_manageip = "172.23.4.41"
    ceph_members = "172.23.47.41,172.23.47.42,172.23.47.43"
    ceph_mon_members = "172.23.47.41,172.23.47.42,172.23.47.43"
    ceph_osd_members = "172.23.47.41,172.23.47.42,172.23.47.43"
    ceph_manageips = "172.23.4.41,172.23.4.42,172.23.4.43"
    ceph_mon_add_members = "172.23.47.60"
    ceph_osd_add_members = "172.23.47.60"
    ceph_manageips_add = "172.23.4.60"
    deploy_conf_file = "/opt/config/rc_" + ceph_deploy_manageip + ".ini"
    deploy_conf = get_conf(deploy_conf_file)

    if not deploy_conf.has_section("ceph"):
        deploy_conf.add_section("ceph")

    deploy_conf.set("ceph", "ceph_members", ceph_members)
    deploy_conf.set("ceph", 'ceph_mon_members', ceph_mon_members)
    deploy_conf.set("ceph", 'ceph_osd_members', ceph_osd_members)
    deploy_conf.set("ceph", 'ceph_manageips', ceph_manageips)
    deploy_conf.set("ceph", 'ceph_mon_add_members', ceph_mon_add_members)
    deploy_conf.set("ceph", "ceph_osd_add_members", ceph_osd_add_members)
    deploy_conf.set("ceph", 'ceph_deploy_manageip', ceph_deploy_manageip)
    deploy_conf.set("ceph", 'ceph_manageips_add', ceph_manageips_add)
    with open(deploy_conf_file, "w") as new_ini:
        deploy_conf.write(new_ini)



def main():
    # clean_nodeslog(params)
    # clean_nodespkg(params)
    # nodesconn(params)
    #hosts_create(params)
    #prepare_hosts(params)
    #parser_dicts(params)
    #prepare_scripts_openstack_deployments(openstack_ver)
    #dispatch_res(params)
    #trigger_exec(params)
    #check_install(params)
    #controller_info(params)
    #clean_nodespkg(params)
    #get_node_deployment_progress("6b2bfd88-3b29-4e42-af60-5f5892be6171")
    update_ini()


if __name__ == '__main__':
    main()