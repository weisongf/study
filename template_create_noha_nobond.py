#!/usr/bin/env python
# -*-coding:utf-8-*-
import ConfigParser
import re
import os

def create_configfile(hostname,\
ntp_server_ip,\
enable_services,\
role_type,\
bond_enable,\
bond_mode,\
manage_vlanid,\
manage_nicname,\
manage_bondname,\
manage_nicname1,\
manage_nicname2,\
manage_ip,\
manage_netmask,\
manage_gateway,\
internal_vlanid,\
internal_nicname,\
internal_bondname,\
internal_nicname1,\
internal_nicname2,\
internal_ip,\
internal_netmask,\
bussiness_nicname,\
bussiness_bondname,\
bussiness_nicname1,\
bussiness_nicname2,\
storage_nicname,\
storage_bondname,\
storage_nicname1,\
storage_nicname2,\
storage_ip,\
storage_netmask,\
endpoint_ip,\
neutron_mode,\
neutron_type,\
enable_ha,\
controller_nums,\
controller_manage_members,\
controller_internal_members,\
controller_internal_vip):
    hostname = hostname
    ntp_server_ip = ntp_server_ip
    enable_services = enable_services
    role_type = role_type
    # bond_enable=yes 此参数有两个值，yes表示启用bond，no表示不bond
    bond_enable = bond_enable
    bond_mode = bond_mode
    manage_vlanid = manage_vlanid
    manage_nicname = manage_nicname
    manage_bondname = manage_bondname
    manage_nicname1 = manage_nicname1
    manage_nicname2 = manage_nicname2
    manage_ip = manage_ip
    manage_netmask = manage_netmask
    manage_gateway = manage_gateway
    internal_vlanid = internal_vlanid
    internal_nicname = internal_nicname
    internal_bondname = internal_bondname
    internal_nicname1 = internal_nicname1
    internal_nicname2 = internal_nicname2
    internal_ip = internal_ip
    internal_netmask = internal_netmask
    bussiness_nicname = bussiness_nicname
    bussiness_bondname = bussiness_bondname
    bussiness_nicname1 = bussiness_nicname1
    bussiness_nicname2 = bussiness_nicname2

    storage_nicname = storage_nicname
    storage_bondname = storage_bondname
    storage_nicname1 = storage_nicname1
    storage_nicname2 = storage_nicname2
    storage_ip = storage_ip
    storage_netmask = storage_netmask
    endpoint_ip = endpoint_ip
    neutron_mode = neutron_mode
    neutron_type = neutron_type

    enable_ha = enable_ha
    controller_nums = controller_nums
    controller_manage_members = controller_manage_members
    controller_internal_members = controller_internal_members
    controller_internal_vip = controller_internal_vip
    # 读取配置文件

    if os.path.exists("template_" + manage_ip + ".ini"):
        os.remove("template_" + manage_ip + ".ini")
    else:
        pass
    # 读取配置文件
    config = ConfigParser.ConfigParser()
    config.read("template_" + manage_ip + ".ini")
    # 写入host片段配置文件
    try:
        config.add_section("host")
        config.set("host", "hostname", hostname)
        config.set("host", "ntp_server_ip", ntp_server_ip)
    except ConfigParser.DuplicateSectionError:
        print("Section 'host' already exists")

    if enable_ha == "no" and bond_enable=="no" :
        if role_type == "controller":
            # 写入components片段配置文件
            try:
                config.add_section("components")
                config.set("components", "enable_services", "db,rabbitmq,keystone,glance,nova,neutron,cinder")
            except ConfigParser.DuplicateSectionError:
                print("Section 'components' already exists")
            # 写入role片段配置文件
            try:
                config.add_section("role")
                config.set("role", "role_type", "controller")
            except ConfigParser.DuplicateSectionError:
                print("Section 'role' already exists")

            # 写入network片段配置文件
            try:
                config.add_section("network")
                config.set("network", "bond_enable", bond_enable)
                config.set("network", "bond_mode", bond_mode)
                config.set("network", "manage_vlanid", manage_vlanid)
                config.set("network", "manage_nicname", manage_nicname)
                config.set("network", "manage_nicname1", manage_nicname1)
                config.set("network", "manage_nicname2", manage_nicname2)
                config.set("network", "manage_ip", manage_ip)
                config.set("network", "manage_netmask", manage_netmask)
                config.set("network", "manage_gateway", manage_gateway)
                config.set("network", "internal_vlanid", internal_vlanid)
                config.set("network", "internal_nicname", internal_nicname)
                config.set("network", "internal_bondname", internal_bondname)
                config.set("network", "internal_nicname1", internal_nicname1)
                config.set("network", "internal_nicname2", internal_nicname2)
                config.set("network", "internal_ip", internal_ip)
                config.set("network", "internal_netmask", internal_netmask)
                config.set("network", "bussiness_nicname", bussiness_nicname)
                config.set("network", "bussiness_bondname", bussiness_bondname)
                config.set("network", "bussiness_nicname1", bussiness_nicname1)
                config.set("network", "bussiness_nicname2", bussiness_nicname2)
                config.set("network", "storage_nicname", storage_nicname)
                config.set("network", "storage_bondname", storage_bondname)
                config.set("network", "storage_nicname1", storage_nicname1)
                config.set("network", "storage_nicname2", storage_nicname2)
                config.set("network", "storage_ip", storage_ip)
                config.set("network", "storage_netmask", storage_netmask)
            except ConfigParser.DuplicateSectionError:
                print("Section 'network' already exists")

            # 写入keystone片段配置文件
            try:
                config.add_section("keystone")
                config.set("keystone", "endpoint_ip", endpoint_ip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'keystone' already exists")

            # 写入glance片段配置文件
            try:
                config.add_section("glance")
            except ConfigParser.DuplicateSectionError:
                print("Section 'glance' already exists")

            # 写入nova片段配置文件
            try:
                config.add_section("nova")
            except ConfigParser.DuplicateSectionError:
                print("Section 'nova' already exists")

            # 写入neutron片段配置文件
            try:
                config.add_section("neutron")
                config.set("neutron", "neutron_mode", "self")
                config.set("neutron", "neutron_type", "vxlan,vlan")
            except ConfigParser.DuplicateSectionError:
                print("Section 'neutron' already exists")

            # 写入cinder片段配置文件
            try:
                config.add_section("cinder")
            except ConfigParser.DuplicateSectionError:
                print("Section 'cinder' already exists")

            # 写入ceph片段配置文件
            try:
                config.add_section("ceph")
            except ConfigParser.DuplicateSectionError:
                print("Section 'ceph' already exists")

            # 写入ha片段配置文件
            try:
                config.add_section("ha")
                config.set("ha", "enable_ha", enable_ha)
                config.set("ha", "controller_nums", controller_nums)
                config.set("ha", "controller_manage_members", controller_manage_members)
                config.set("ha", "controller_internal_members", controller_internal_members)
                config.set("ha", "controller_internal_vip", controller_internal_vip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'ha' already exists")
        elif role_type == "network":
            try:
                config.add_section("components")
                config.set("components", "enable_services", "neutron")
            except ConfigParser.DuplicateSectionError:
                print("Section 'components' already exists")
            try:
                config.add_section("role")
                config.set("role", "role_type", "network")
            except ConfigParser.DuplicateSectionError:
                print("Section 'role' already exists")

            # 写入network片段配置文件
            try:
                config.add_section("network")
                config.set("network", "bond_enable", bond_enable)
                config.set("network", "bond_mode", bond_mode)
                config.set("network", "manage_vlanid", manage_vlanid)
                config.set("network", "manage_nicname", manage_nicname)
                config.set("network", "manage_nicname1", manage_nicname1)
                config.set("network", "manage_nicname2", manage_nicname2)
                config.set("network", "manage_ip", manage_ip)
                config.set("network", "manage_netmask", manage_netmask)
                config.set("network", "manage_gateway", manage_gateway)
                config.set("network", "internal_vlanid", internal_vlanid)
                config.set("network", "internal_nicname", internal_nicname)
                config.set("network", "internal_bondname", internal_bondname)
                config.set("network", "internal_nicname1", internal_nicname1)
                config.set("network", "internal_nicname2", internal_nicname2)
                config.set("network", "internal_ip", internal_ip)
                config.set("network", "internal_netmask", internal_netmask)
                config.set("network", "bussiness_nicname", bussiness_nicname)
                config.set("network", "bussiness_bondname", bussiness_bondname)
                config.set("network", "bussiness_nicname1", bussiness_nicname1)
                config.set("network", "bussiness_nicname2", bussiness_nicname2)
                config.set("network", "storage_nicname", storage_nicname)
                config.set("network", "storage_bondname", storage_bondname)
                config.set("network", "storage_nicname1", storage_nicname1)
                config.set("network", "storage_nicname2", storage_nicname2)
                config.set("network", "storage_ip", storage_ip)
                config.set("network", "storage_netmask", storage_netmask)
            except ConfigParser.DuplicateSectionError:
                print("Section 'network' already exists")

            # 写入keystone片段配置文件
            try:
                config.add_section("keystone")
                config.set("keystone", "endpoint_ip", endpoint_ip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'keystone' already exists")

            # 写入glance片段配置文件
            try:
                config.add_section("glance")
            except ConfigParser.DuplicateSectionError:
                print("Section 'glance' already exists")

            # 写入nova片段配置文件
            try:
                config.add_section("nova")
            except ConfigParser.DuplicateSectionError:
                print("Section 'nova' already exists")

            # 写入neutron片段配置文件
            try:
                config.add_section("neutron")
                config.set("neutron", "neutron_mode", "self")
                config.set("neutron", "neutron_type", "vxlan,vlan")
            except ConfigParser.DuplicateSectionError:
                print("Section 'neutron' already exists")

            # 写入cinder片段配置文件
            try:
                config.add_section("cinder")
            except ConfigParser.DuplicateSectionError:
                print("Section 'cinder' already exists")

            # 写入ceph片段配置文件
            try:
                config.add_section("ceph")
            except ConfigParser.DuplicateSectionError:
                print("Section 'ceph' already exists")

            # 写入ha片段配置文件
            try:
                config.add_section("ha")
                config.set("ha", "enable_ha", enable_ha)
                config.set("ha", "controller_nums", controller_nums)
                config.set("ha", "controller_manage_members", controller_manage_members)
                config.set("ha", "controller_internal_members", controller_internal_members)
                config.set("ha", "controller_internal_vip", controller_internal_vip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'ha' already exists")
        elif role_type == "compute":
            try:
                config.add_section("components")
                config.set("components", "enable_services", "nova,neutron")
            except ConfigParser.DuplicateSectionError:
                print("Section 'components' already exists")
            try:
                config.add_section("role")
                config.set("role", "role_type", "compute")
            except ConfigParser.DuplicateSectionError:
                print("Section 'role' already exists")

            # 写入network片段配置文件
            try:
                config.add_section("network")
                config.set("network", "bond_enable", bond_enable)
                config.set("network", "bond_mode", bond_mode)
                config.set("network", "manage_vlanid", manage_vlanid)
                config.set("network", "manage_nicname", manage_nicname)
                config.set("network", "manage_nicname1", manage_nicname1)
                config.set("network", "manage_nicname2", manage_nicname2)
                config.set("network", "manage_ip", manage_ip)
                config.set("network", "manage_netmask", manage_netmask)
                config.set("network", "manage_gateway", manage_gateway)
                config.set("network", "internal_vlanid", internal_vlanid)
                config.set("network", "internal_nicname", internal_nicname)
                config.set("network", "internal_bondname", internal_bondname)
                config.set("network", "internal_nicname1", internal_nicname1)
                config.set("network", "internal_nicname2", internal_nicname2)
                config.set("network", "internal_ip", internal_ip)
                config.set("network", "internal_netmask", internal_netmask)
                config.set("network", "bussiness_nicname", bussiness_nicname)
                config.set("network", "bussiness_bondname", bussiness_bondname)
                config.set("network", "bussiness_nicname1", bussiness_nicname1)
                config.set("network", "bussiness_nicname2", bussiness_nicname2)
                config.set("network", "storage_nicname", storage_nicname)
                config.set("network", "storage_bondname", storage_bondname)
                config.set("network", "storage_nicname1", storage_nicname1)
                config.set("network", "storage_nicname2", storage_nicname2)
                config.set("network", "storage_ip", storage_ip)
                config.set("network", "storage_netmask", storage_netmask)
            except ConfigParser.DuplicateSectionError:
                print("Section 'network' already exists")

            # 写入keystone片段配置文件
            try:
                config.add_section("keystone")
                config.set("keystone", "endpoint_ip", endpoint_ip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'keystone' already exists")

            # 写入glance片段配置文件
            try:
                config.add_section("glance")
            except ConfigParser.DuplicateSectionError:
                print("Section 'glance' already exists")

            # 写入nova片段配置文件
            try:
                config.add_section("nova")
            except ConfigParser.DuplicateSectionError:
                print("Section 'nova' already exists")

            # 写入neutron片段配置文件
            try:
                config.add_section("neutron")
                config.set("neutron", "neutron_mode", "self")
                config.set("neutron", "neutron_type", "vxlan,vlan")
            except ConfigParser.DuplicateSectionError:
                print("Section 'neutron' already exists")

            # 写入cinder片段配置文件
            try:
                config.add_section("cinder")
            except ConfigParser.DuplicateSectionError:
                print("Section 'cinder' already exists")

            # 写入ceph片段配置文件
            try:
                config.add_section("ceph")
            except ConfigParser.DuplicateSectionError:
                print("Section 'ceph' already exists")

            # 写入ha片段配置文件
            try:
                config.add_section("ha")
                config.set("ha", "enable_ha", enable_ha)
                config.set("ha", "controller_nums", controller_nums)
                config.set("ha", "controller_manage_members", controller_manage_members)
                config.set("ha", "controller_internal_members", controller_internal_members)
                config.set("ha", "controller_internal_vip", controller_internal_vip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'ha' already exists")
        elif role_type == "ceph":
            try:
                config.add_section("components")
                config.set("components", "enable_services", "ceph")
            except ConfigParser.DuplicateSectionError:
                print("Section 'components' already exists")
            try:
                config.add_section("role")
                config.set("role", "role_type", "ceph")
            except ConfigParser.DuplicateSectionError:
                print("Section 'role' already exists")

                # 写入network片段配置文件
            try:
                config.add_section("network")
                config.set("network", "bond_enable", bond_enable)
                config.set("network", "bond_mode", bond_mode)
                config.set("network", "manage_vlanid", manage_vlanid)
                config.set("network", "manage_nicname", manage_nicname)
                config.set("network", "manage_nicname1", manage_nicname1)
                config.set("network", "manage_nicname2", manage_nicname2)
                config.set("network", "manage_ip", manage_ip)
                config.set("network", "manage_netmask", manage_netmask)
                config.set("network", "manage_gateway", manage_gateway)
                config.set("network", "internal_vlanid", internal_vlanid)
                config.set("network", "internal_nicname", internal_nicname)
                config.set("network", "internal_bondname", internal_bondname)
                config.set("network", "internal_nicname1", internal_nicname1)
                config.set("network", "internal_nicname2", internal_nicname2)
                config.set("network", "internal_ip", internal_ip)
                config.set("network", "internal_netmask", internal_netmask)
                config.set("network", "bussiness_nicname", bussiness_nicname)
                config.set("network", "bussiness_bondname", bussiness_bondname)
                config.set("network", "bussiness_nicname1", bussiness_nicname1)
                config.set("network", "bussiness_nicname2", bussiness_nicname2)
                config.set("network", "storage_nicname", storage_nicname)
                config.set("network", "storage_bondname", storage_bondname)
                config.set("network", "storage_nicname1", storage_nicname1)
                config.set("network", "storage_nicname2", storage_nicname2)
                config.set("network", "storage_ip", storage_ip)
                config.set("network", "storage_netmask", storage_netmask)
            except ConfigParser.DuplicateSectionError:
                print("Section 'network' already exists")

                # 写入keystone片段配置文件
            try:
                config.add_section("keystone")
                config.set("keystone", "endpoint_ip", endpoint_ip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'keystone' already exists")

                # 写入glance片段配置文件
            try:
                config.add_section("glance")
            except ConfigParser.DuplicateSectionError:
                print("Section 'glance' already exists")

                # 写入nova片段配置文件
            try:
                config.add_section("nova")
            except ConfigParser.DuplicateSectionError:
                print("Section 'nova' already exists")

                # 写入neutron片段配置文件
            try:
                config.add_section("neutron")
                config.set("neutron", "neutron_mode", "self")
                config.set("neutron", "neutron_type", "vxlan,vlan")
            except ConfigParser.DuplicateSectionError:
                print("Section 'neutron' already exists")

                # 写入cinder片段配置文件
            try:
                config.add_section("cinder")
            except ConfigParser.DuplicateSectionError:
                print("Section 'cinder' already exists")

                # 写入ceph片段配置文件
            try:
                config.add_section("ceph")
            except ConfigParser.DuplicateSectionError:
                print("Section 'ceph' already exists")

                # 写入ha片段配置文件
            try:
                config.add_section("ha")
                config.set("ha", "enable_ha", enable_ha)
                config.set("ha", "controller_nums", controller_nums)
                config.set("ha", "controller_manage_members", controller_manage_members)
                config.set("ha", "controller_internal_members", controller_internal_members)
                config.set("ha", "controller_internal_vip", controller_internal_vip)
            except ConfigParser.DuplicateSectionError:
                print("Section 'ha' already exists")
    config.write(open("template_" + manage_ip + ".ini", "w"))

role_type_list = ["controller","network","compute","ceph"]
hostname_list = ["controller1","network1","network2","compute1","compute2","ceph1","ceph2","ceph3"]
manage_ipaddress_list=["172.23.30.69","172.23.30.70","172.23.30.71","172.23.30.72","172.23.30.73","172.23.30.74","172.23.30.75","172.23.30.76"]
internal_ipaddress_list=["172.23.47.50","172.23.47.46","172.23.47.47","172.23.47.48","172.23.47.49","172.23.47.51","172.23.47.52","172.23.47.53"]
storage_ipaddress_list=["172.23.48.23","172.23.48.19","172.23.48.20","172.23.48.21","172.23.48.22","172.23.48.24","172.23.48.25","172.23.48.26"]

for index in range(0,len(hostname_list),1):
    if re.match(r'^controller',hostname_list[index],re.I):
        create_configfile(hostname_list[index], \
                          "172.23.30.77", \
                          "db,rabbitmq,keystone,glance,nova,neutron,cinder", \
                          "controller", \
                          "no", \
                          "", \
                          "", \
                          "eth0", \
                          "bondadmin", \
                          "", \
                          "", \
                          manage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.254", \
                          "", \
                          "eth1", \
                          "bondinternal", \
                          "", \
                          "", \
                          internal_ipaddress_list[index], \
                          "255.255.255.0", \
                          "eth2", \
                          "bondbussiness", \
                          "", \
                          "", \
                          "eth2", \
                          "bondstorage", \
                          "", \
                          "", \
                          storage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.69", \
                          "self", \
                          "vxlan,vlan", \
                          "no", \
                          "1", \
                          "172.23.30.69", \
                          "", \
                          "")
    if re.match(r'^network', hostname_list[index],re.I):
        create_configfile(hostname_list[index], \
                          "172.23.30.77", \
                          "neutron", \
                          "network", \
                          "no", \
                          "", \
                          "", \
                          "eth0", \
                          "bondadmin", \
                          "", \
                          "", \
                          manage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.254", \
                          "", \
                          "eth1", \
                          "bondinternal", \
                          "", \
                          "", \
                          internal_ipaddress_list[index], \
                          "255.255.255.0", \
                          "eth2", \
                          "bondbussiness", \
                          "", \
                          "", \
                          "eth2", \
                          "bondstorage", \
                          "", \
                          "", \
                          storage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.69", \
                          "self", \
                          "vxlan,vlan", \
                          "no", \
                          "1", \
                          "172.23.30.69", \
                          "",\
                          "")
    if re.match(r'^compute', hostname_list[index],re.I):
        create_configfile(hostname_list[index], \
                          "172.23.30.77", \
                          "nova", \
                          "compute", \
                          "no", \
                          "", \
                          "", \
                          "eth0", \
                          "bondadmin", \
                          "", \
                          "", \
                          manage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.254", \
                          "", \
                          "eth1", \
                          "bondinternal", \
                          "", \
                          "", \
                          internal_ipaddress_list[index], \
                          "255.255.255.0", \
                          "eth2", \
                          "bondbussiness", \
                          "", \
                          "", \
                          "eth2", \
                          "bondstorage", \
                          "", \
                          "", \
                          storage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.69", \
                          "self", \
                          "vxlan,vlan", \
                          "no", \
                          "1", \
                          "172.23.30.69", \
                          "", \
                          "")
    if re.match(r'^ceph', hostname_list[index],re.I):
        create_configfile(hostname_list[index], \
                          "172.23.30.77", \
                          "ceph", \
                          "ceph", \
                          "no", \
                          "", \
                          "", \
                          "eth0", \
                          "bondadmin", \
                          "", \
                          "", \
                          manage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.254", \
                          "", \
                          "eth1", \
                          "bondinternal", \
                          "", \
                          "", \
                          internal_ipaddress_list[index], \
                          "255.255.255.0", \
                          "eth2", \
                          "bondbussiness", \
                          "", \
                          "", \
                          "eth2", \
                          "bondstorage", \
                          "", \
                          "", \
                          storage_ipaddress_list[index], \
                          "255.255.255.0", \
                          "172.23.30.69", \
                          "self", \
                          "vxlan,vlan", \
                          "no", \
                          "1", \
                          "172.23.30.69", \
                          "", \
                          "")