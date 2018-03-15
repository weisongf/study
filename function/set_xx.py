#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging

logger = logging.getLogger(__name__)


RODS_CONF = "/etc/rod_server/rods.conf"

def get_config():
    config = ConfigParser.ConfigParser()
    config.read(RODS_CONF)

    return config


def get_conf(filename):
    conf = ConfigParser.ConfigParser()
    conf.read(filename)

    return conf

#更新ceph 配置文件信息
def ceph_update(ceph_add_members,ceph_add_members_old):
    ceph_add_node = []
    for i in ceph_add_members:
        if i not in ceph_add_members_old:
            ceph_add_node.append(i)

    if ceph_add_node:
        ceph_new_str = ceph_add_members_old + "," + ",".join(ceph_add_node)
    else:
        ceph_new_str = ceph_add_members_old
    return  ceph_new_str

env_conf_file = "C:\Users\song.w\PycharmProjects\study\/function\env_conf_file_82"
env_conf = get_conf(env_conf_file)

ceph_mon_add_members = ["172.23.47.58"]
ceph_osd_add_members = ["172.23.47.58","172.23.47.60","172.23.47.61"]
ceph_manageips_add = ["172.23.4.58","172.23.4.59","172.23.4.60"]

# ceph配置信息
ceph_deploy_ip = env_conf.get('DEFAULT', 'ceph_deploy_ip')
ceph_members_old = env_conf.get('DEFAULT', 'ceph_members')
ceph_mon_members_old = env_conf.get('DEFAULT', 'ceph_mon_members')
ceph_osd_members_old = env_conf.get('DEFAULT', 'ceph_osd_members')
ceph_manageips_old = env_conf.get('DEFAULT', 'ceph_manageips')
ceph_deploy_manageip =  ceph_manageips_old.split(",")[0]
ceph_mon_add = []
ceph_osd_add = []
#获得新增的ceph节点信息
ceph_add = list(set(ceph_mon_add_members) | set(ceph_osd_add_members))
#ceph_members = ceph_members_old + "," + ",".join(ceph_add)

#print ("ceph_add:%s" % ceph_add)
#ceph_members_new = set(ceph_members_old.split(','))|set(ceph_add)



ceph_mon_members = ceph_update(ceph_mon_add_members,ceph_mon_members_old)
print ("ceph_mon_members:",ceph_mon_members)

ceph_osd_members = ceph_update(ceph_osd_add_members,ceph_osd_members_old)
print ("ceph_osd_members:",ceph_osd_members)

ceph_manageips = ceph_update(ceph_manageips_add,ceph_manageips_old)
print ("ceph_manageips:",ceph_manageips)

ceph_members = ceph_update(ceph_add,ceph_members_old)
print ("ceph_members:",ceph_members)
logger.info("ceph_mon_members:%s,ceph_osd_members:%s,ceph_manageips:%s,ceph_members:%s",(ceph_mon_members,ceph_osd_members,ceph_manageips,ceph_members))
#
#
# ceph_manageips_add = ",".join(ceph_manageips_add)
# ceph_manageips = ceph_manageips_old + "," + ceph_manageips_add

##############################################
        # ceph_mon_add = []
        # ceph_osd_add = []
        # ceph_manageips_new = []
        # for node in nodes_list:
        #     enable_services = node.get('component')
        #     if 'storage' in node.get('type').split(","):
        #         for nic in node.get('nicbond'):
        #             if 'storage' == nic.get('netflag'):
        #                 storage_ip = nic.get('ip')
        #                 if 'ceph-mon' in enable_services.split(","):
        #                     ceph_mon_add_members.append(storage_ip)
        #                 if 'ceph-osd' in enable_services.split(","):
        #                     ceph_osd_add_members.append(storage_ip)
        #             elif 'admin' == nic.get('netflag'):
        #                 ceph_manageips_add.append(nic.get('ip'))
        # # ceph配置信息
        # ceph_deploy_ip = env_conf.get('DEFAULT', 'ceph_deploy_ip')
        # ceph_members_old = env_conf.get('DEFAULT', 'ceph_members')
        # ceph_mon_members_old = env_conf.get('DEFAULT', 'ceph_mon_members')
        # ceph_osd_members_old = env_conf.get('DEFAULT', 'ceph_osd_members')
        # ceph_manageips_old = env_conf.get('DEFAULT', 'ceph_manageips')
        # ceph_deploy_manageip =  ceph_manageips_old.split(",")[0]
        #
        # ceph_add = list(set(ceph_mon_add_members) | set(ceph_osd_add_members))
        # #获得新增的ceph节点信息
        # for i in ceph_mon_add_members:
        #     if i not in ceph_mon_members_old:
        #         ceph_mon_add.append(i)
        #
        # for i in ceph_osd_add_members:
        #     if i not in ceph_osd_members_old:
        #         ceph_osd_add.append(i)
        #
        # for i in ceph_manageips_add:
        #     if i not in ceph_manageips_old:
        #         ceph_manageips_new.append(i)
        # ##
        # if ceph_mon_add:
        #     ceph_mon_members = ceph_mon_members_old + "," + ",".join(ceph_mon_add)
        # else:
        #     ceph_mon_members = ceph_mon_members_old
        #
        # if ceph_osd_add:
        #     ceph_osd_members = ceph_osd_members_old + "," + ",".join(ceph_osd_add)
        # else:
        #     ceph_osd_members = ceph_osd_members_old
        #
        #
        # if ceph_manageips_new:
        #     ceph_manageips = ceph_manageips_old + "," + ",".join(ceph_manageips_new)
        # else:
        #     ceph_manageips = ceph_manageips_old
        #
        # ceph_members = ceph_members_old + "," + ",".join(ceph_add)
        #
        # ceph_mon_add_members = ",".join(ceph_mon_add_members)
        # ceph_osd_add_members = ",".join(ceph_osd_add_members)
        #
        #
        # ceph_manageips_add = ",".join(ceph_manageips_add)