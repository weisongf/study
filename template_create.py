#!/usr/bin/env python
# -*-coding:utf-8-*-
import ConfigParser

def create_configfile(role_type,enable_ha):

#读取配置文件
config=ConfigParser.ConfigParser()
config.read("template_10.10.0.10.ini")

#写入host片段配置文件
try:
    config.add_section("host")
    config.set("host","hostname","hl-controller1")
except ConfigParser.DuplicateSectionError:
    print("Section 'host' already exists")

#写入components片段配置文件
try:
    config.add_section("components")
    config.set("components","enable","db,rabbitmq,keystone,glance,nova,neutron,cinder")
except ConfigParser.DuplicateSectionError:
    print("Section 'components' already exists")

#写入role片段配置文件
try:
    config.add_section("role")
    config.set("role","role_type","controller,network")
except ConfigParser.DuplicateSectionError:
    print("Section 'role' already exists")

#写入network片段配置文件
try:
    config.add_section("network")
    config.set("network","bond_mode","1")
    config.set("network","manage_vlanid","100")
    config.set("network","manage_nicname1","eth0")
    config.set("network","manage_nicname2", "eth1")
    config.set("network","manage_ip", "172.200.4.10")
    config.set("network","manage_netmask", "255.255.255.0")
    config.set("network","manage_gateway", "172.200.4.254")
    config.set("network","internal_vlanid","2000")
    config.set("network","internal_nicname1","eth2")
    config.set("network","internal_nicname2","eth3")
    config.set("network","internal_ip", "10.10.0.11")
    config.set("network","internal_netmask", "255.255.255.0")
    config.set("network", "bussiness_nicname1", "eth4")
    config.set("network", "bussiness_nicname2", "eth5")
    config.set("network", "storage_nicname1", "eth6")
    config.set("network", "storage_nicname2", "eth7")
    config.set("network", "storage_ip", "20.10.0.10")
    config.set("network", "storage_netmask", "255.255.255.0")
except ConfigParser.DuplicateSectionError:
    print("Section 'network' already exists")

#写入keystone片段配置文件
try:
    config.add_section("keystone")
    config.set("keystone","endpoint_ip","172.200.4.10")
except ConfigParser.DuplicateSectionError:
    print("Section 'keystone' already exists")

#写入glance片段配置文件
try:
    config.add_section("glance")
except ConfigParser.DuplicateSectionError:
    print("Section 'glance' already exists")

#写入nova片段配置文件
try:
    config.add_section("nova")
except ConfigParser.DuplicateSectionError:
    print("Section 'nova' already exists")

#写入neutron片段配置文件
try:
    config.add_section("neutron")
    config.set("neutron", "neutron_mode", "self")
    config.set("neutron", "neutron_type", "vxlan,vlan")
except ConfigParser.DuplicateSectionError:
    print("Section 'neutron' already exists")

#写入cinder片段配置文件
try:
    config.add_section("cinder")
except ConfigParser.DuplicateSectionError:
    print("Section 'cinder' already exists")

#写入ceph片段配置文件
try:
    config.add_section("ceph")
except ConfigParser.DuplicateSectionError:
    print("Section 'ceph' already exists")

#写入ha片段配置文件
try:
    config.add_section("ha")
    config.set("ha", "enable_ha", "no")
    config.set("ha", "controller_nums", "1")
    config.set("ha", "controller_members", "172.200.4.10")
    config.set("ha", "controller_internal_vip", "")
except ConfigParser.DuplicateSectionError:
    print("Section 'ha' already exists")
#写入配置文件
config.write(open("template_10.10.0.10.ini", "w"))

enable_ha=config.get("ha","enable_ha")
neutron_mode=config.get("neutron","neutron_mode")
endpoint_ip=config.get("keystone","endpoint_ip")


print((enable_ha,neutron_mode+"\n"+endpoint_ip))