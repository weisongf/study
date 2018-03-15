#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
import re

hosts_openstack="/opt/lib/hosts_openstack"
hosts_ceph="/opt/lib/hosts_ceph"

role_type_list = ["controller","network","compute","ceph"]
hostname_list = ["controller1","network1","network2","compute1","compute2","ceph1","ceph2","ceph3"]
manage_ipaddress_list=["172.23.30.69","172.23.30.70","172.23.30.71","172.23.30.72","172.23.30.73","172.23.30.74","172.23.30.75","172.23.30.76"]
internal_ipaddress_list=["172.23.47.50","172.23.47.46","172.23.47.47","172.23.47.48","172.23.47.49","172.23.47.51","172.23.47.52","172.23.47.53"]
storage_ipaddress_list=["172.23.48.23","172.23.48.19","172.23.48.20","172.23.48.21","172.23.48.22","172.23.48.24","172.23.48.25","172.23.48.26"]

def create_hosts_openstack():
    if os.path.exists(hosts_openstack):
        os.remove(hosts_openstack)
    else:
        pass
    with open(hosts_openstack,'a') as f:
        f.write('127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4'+'\n'\
                '::1         localhost localhost.localdomain localhost6 localhost6.localdomain6'+'\n' )
        for index_num in range(0,len(hostname_list),1):
            if re.match(r'^controller|^network|^compute',hostname_list[index_num],re.I):
                f.write(internal_ipaddress_list[index_num] + ' '+hostname_list[index_num]+'\n')
            else:
                f.write(storage_ipaddress_list[index_num] + ' ' + hostname_list[index_num] + '\n')
    print("Create hosts_openstack file successfull")
    return

def create_hosts_ceph():
    if os.path.exists(hosts_ceph):
        os.remove(hosts_ceph)
    else:
        pass
    with open(hosts_ceph,'a') as f:
        f.write('127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4'+'\n'\
                '::1         localhost localhost.localdomain localhost6 localhost6.localdomain6'+'\n' )
        for index_num in range(0,len(hostname_list),1):
            f.write(storage_ipaddress_list[index_num] + ' '+hostname_list[index_num]+'\n')
    print("Create hosts_ceph file successfull")
    return

create_hosts_openstack()
create_hosts_ceph()