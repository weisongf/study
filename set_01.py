#!/usr/bin/env python
# -*- coding:utf-8-*-
list_con = ["172.23.48.80","172.23.48.81","172.23.48.82","172.23.48.83"]
list_net = ["172.23.48.81","172.23.48.82","172.23.48.83"]
list_com = ["172.23.48.81","172.23.48.82","172.23.48.83","172.23.48.87"]
list_stor = ["172.23.48.84","172.23.48.85","172.23.48.86"]

set_con = set(list_con)
set_net = set(list_net)
set_com = set(list_com)
set_stor = set(list_stor)
net = set_net-set_con
print "set_net-set_con" ,net
print "set_com-set_con" ,set_com-set_con


func = lambda x,y:x*y
print func(20,10)

filter_list = filter(lambda x:x % 2 ==0,xrange(1,13))

print filter_list

cmd = "cat >> /etc/sysconfig/network-scripts/ifcfg-ens160 <<__SW__
DEVICE=ens160
BOOTPROTO=static
IPADDR=172.23.4.122
NETMASK=255.255.255.0
GATEWAY=172.23.4.254
ONBOOT=yes
TYPE=Ethernet
NM_CONTROLLED=no
__SW__"

ls /root/nic_bak/

