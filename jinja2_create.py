#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os
import json
import ConfigParser
import re

if __name__ == '__main__':
    j2_path = rc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')

    j2_env = Environment(loader=FileSystemLoader(j2_path))

    nodes = {
        "DEFAULT": {
            "openstack_version": "Mitaka",
            "bond_enable": "true",
            "ha_enable": "true",
            "bond_mode": "1",
            "network_mode": "self",
            "network_type": "vxlan,vlan"
        },

        "host": {
            "hostname": "controller1",
            "ntp_server_ip": "172.23.30.77",
            "server_id": "1a14025d-cf26-4bbb-b27a-e3496e245806",
            "upstream_internal_ip": "172.23.47.69",
            "upstream_manage_ip": "172.23.30.69"
        },
        "components": {
            "enable_services": "db,rabbitmq,keystone,glance-api,glance-registry,nova-api,nova-conductor,nova-consoleauth,nova-novncproxy,nova-scheduler,nova-compute,neutron-server,neutron-metadata-agent,neutron-dhcp-agent,neutron-l3-agent,neutron-openvswitch-agent,cinder-api,cinder-scheduler,cinder-volume"
        },
        "role": {
            "role_type": "storage,controller,compute"
        },
        "network": {
            "manage_vlanid": "100",
            "manage_bondname": "bondadmin",
            "manage_nicname1": "eth0",
            "manage_nicname2": "eth1",
            "manage_ip": "172.23.30.69 ",
            "manage_netmask": "255.255.255.0",
            "manage_gateway": "172.23.30.254",
            "internal_vlanid": "2000",
            "internal_bondname": "bondinternal",
            "internal_nicname1": "eth2",
            "internal_nicname2": "eth3",
            "internal_ip": "10.10.0.11",
            "internal_netmask": "255.255.255.0",
            "bussiness_bondname": "bondbussiness",
            "bussiness_nicname1": "eth4",
            "bussiness_nicname2": "eth5",
            "storage_bondname":"bondstorage",
            "storage_nicname1": "eth6",
            "storage_nicname2": "eth7",
            "storage_ip": "20.10.0.10",
            "storage_netmask": "255.255.255.0"
        },
        "ceph":{
            "ceph_deploy_ip":"20.10.0.10",
            "ceph_members":"20.10.0.10,20.10.0.11,20.10.0.12",
            "ceph_mon_members":"20.10.0.10,20.10.0.11,20.10.0.12",
            "ceph_osd_members":"20.10.0.10,20.10.0.11,20.10.0.12"

        },
        "ha": {
            "controller_nums": "3",
            "controller_manage_members": "172.200.4.11,172.200.4.12,172.200.4.13",
            "controller_internal_members": "10.10.0.11,10.10.0.12,10.10.0.13",
            "controller_internal_vip": "10.10.0.10"
        }
    }
    print(nodes['network']['manage_ip'])
    manage_ip = nodes['network']['manage_ip']
    manage_ip = ''.join(manage_ip.split())
    hostname = nodes['host']['hostname']
    ntp_server_ip = nodes['host']['ntp_server_ip']
    server_id = nodes['host']['server_id']
    upstream_internal_ip = nodes['host']['upstream_internal_ip']
    upstream_manage_ip = nodes['host']['upstream_manage_ip']
    openstack_version = nodes['DEFAULT']['openstack_version']
    bond_enable = nodes['DEFAULT']['bond_enable']
    bond_mode = nodes['DEFAULT']['bond_mode']
    ha_enable = nodes['DEFAULT']['ha_enable']
    network_mode = nodes['DEFAULT']['network_mode']
    network_type = nodes['DEFAULT']['network_type']
    enable_services=nodes['components']['enable_services']
    role_type=nodes['role']['role_type']
    manage_vlanid=nodes['network']['manage_vlanid']
    manage_nicname1 = nodes['network']['manage_nicname1']
    manage_nicname2 = nodes['network']['manage_nicname2']
    manage_netmask = nodes['network']['manage_netmask']
    manage_gateway = nodes['network']['manage_gateway']
    internal_vlanid= nodes['network']['internal_vlanid']
    internal_nicname1 = nodes['network']['internal_nicname1']
    internal_nicname2 = nodes['network']['internal_nicname2']
    internal_ip= nodes['network']['internal_ip']
    internal_netmask = nodes['network']['internal_netmask']
    bussiness_nicname1 = nodes['network']['bussiness_nicname1']
    bussiness_nicname2 = nodes['network']['bussiness_nicname2']
    storage_nicname1 = nodes['network']['storage_nicname1']
    storage_nicname2 = nodes['network']['storage_nicname2']
    storage_ip = nodes['network']['storage_ip']
    storage_netmask = nodes['network']['storage_netmask']
    ceph_deploy_ip = nodes['ceph']['ceph_deploy_ip']
    ceph_members = nodes['ceph']['ceph_members']
    ceph_mon_members = nodes['ceph']['ceph_mon_members']
    ceph_osd_members = nodes['ceph']['ceph_osd_members']
    controller_internal_members = nodes['ha']['controller_internal_members'].split(",")
    controller_internal_vip=nodes['ha']['controller_internal_vip']

    print("controller_internal_members=",controller_internal_members)
    for i in range(0,len(controller_internal_members),1):
        print(controller_internal_members[i])
    if openstack_version == 'Mitaka':
        if re.match(r'(^yes|^Yes|^True|^true)',ha_enable) :
            ha_enable = "true"
            if re.match(r'(^yes|^Yes|^True|^true)',bond_enable) :
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_mitaka.ini').render(openstack_version=openstack_version,
                                                                          ha_enable = ha_enable,
                                                                          bond_enable=bond_enable,
                                                                          bond_mode=bond_mode,
                                                                          role_type=role_type,
                                                                          network_mode = network_mode,
                                                                          network_type = network_type,
                                                                          enable_services=enable_services,
                                                                          hostname = hostname,
                                                                          ntp_server_ip = ntp_server_ip,
                                                                          server_id = server_id,
                                                                          upstream_internal_ip=upstream_internal_ip,
                                                                          upstream_manage_ip=upstream_manage_ip,
                                                                          controller_internal_members=controller_internal_members,
                                                                          controller_internal_vip=controller_internal_vip,
                                                                          manage_vlanid = manage_vlanid,
                                                                          manage_nicname1 = manage_nicname1,
                                                                          manage_nicname2 = manage_nicname2,
                                                                          manage_ip=manage_ip,
                                                                          manage_netmask = manage_netmask,
                                                                          manage_gateway = manage_gateway,
                                                                          internal_vlanid = internal_vlanid,
                                                                          internal_nicname1 = internal_nicname1,
                                                                          internal_nicname2 = internal_nicname2,
                                                                          internal_ip = internal_ip,
                                                                          internal_netmask = internal_netmask,
                                                                          bussiness_nicname1 = bussiness_nicname1,
                                                                          bussiness_nicname2 = bussiness_nicname2,
                                                                          storage_nicname1 = storage_nicname1,
                                                                          storage_nicname2 = storage_nicname2,
                                                                          storage_ip = storage_ip,
                                                                          storage_netmask = storage_netmask,
                                                                          ceph_deploy_ip = ceph_deploy_ip,
                                                                          ceph_members = ceph_members,
                                                                          ceph_mon_members = ceph_mon_members,
                                                                          ceph_osd_members = ceph_osd_members
                                                                        ))
            else:
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_mitaka.ini').render(openstack_version=openstack_version,
                                                                          ha_enable = ha_enable,
                                                                          bond_enable=bond_enable,
                                                                          bond_mode=bond_mode,
                                                                          role_type=role_type,
                                                                          network_mode = network_mode,
                                                                          network_type = network_type,
                                                                          enable_services=enable_services,
                                                                          hostname = hostname,
                                                                          ntp_server_ip = ntp_server_ip,
                                                                          server_id = server_id,
                                                                          upstream_internal_ip=upstream_internal_ip,
                                                                          upstream_manage_ip=upstream_manage_ip,
                                                                          controller_internal_members=controller_internal_members,
                                                                          controller_internal_vip=controller_internal_vip,
                                                                          manage_vlanid = manage_vlanid,
                                                                          manage_nicname1 = manage_nicname1,
                                                                          manage_nicname2 = manage_nicname2,
                                                                          manage_ip=manage_ip,
                                                                          manage_netmask = manage_netmask,
                                                                          manage_gateway = manage_gateway,
                                                                          internal_vlanid = internal_vlanid,
                                                                          internal_nicname1 = internal_nicname1,
                                                                          internal_nicname2 = internal_nicname2,
                                                                          internal_ip = internal_ip,
                                                                          internal_netmask = internal_netmask,
                                                                          bussiness_nicname1 = bussiness_nicname1,
                                                                          bussiness_nicname2 = bussiness_nicname2,
                                                                          storage_nicname1 = storage_nicname1,
                                                                          storage_nicname2 = storage_nicname2,
                                                                          storage_ip = storage_ip,
                                                                          storage_netmask = storage_netmask,
                                                                          ceph_deploy_ip = ceph_deploy_ip,
                                                                          ceph_members = ceph_members,
                                                                          ceph_mon_members = ceph_mon_members,
                                                                          ceph_osd_members = ceph_osd_members
                                                                        ))
        else:
            ha_enable = "false"
            if re.match(r'(^yes|^Yes|^True|^true)',bond_enable) :
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_mitaka.ini').render(openstack_version=openstack_version,
                                                                          ha_enable = ha_enable,
                                                                          bond_enable=bond_enable,
                                                                          bond_mode=bond_mode,
                                                                          role_type=role_type,
                                                                          network_mode = network_mode,
                                                                          network_type = network_type,
                                                                          enable_services=enable_services,
                                                                          hostname = hostname,
                                                                          ntp_server_ip = ntp_server_ip,
                                                                          server_id = server_id,
                                                                          upstream_internal_ip=upstream_internal_ip,
                                                                          upstream_manage_ip=upstream_manage_ip,
                                                                          controller_internal_members=controller_internal_members,
                                                                          controller_internal_vip=controller_internal_vip,
                                                                          manage_vlanid = manage_vlanid,
                                                                          manage_nicname1 = manage_nicname1,
                                                                          manage_nicname2 = manage_nicname2,
                                                                          manage_ip=manage_ip,
                                                                          manage_netmask = manage_netmask,
                                                                          manage_gateway = manage_gateway,
                                                                          internal_vlanid = internal_vlanid,
                                                                          internal_nicname1 = internal_nicname1,
                                                                          internal_nicname2 = internal_nicname2,
                                                                          internal_ip = internal_ip,
                                                                          internal_netmask = internal_netmask,
                                                                          bussiness_nicname1 = bussiness_nicname1,
                                                                          bussiness_nicname2 = bussiness_nicname2,
                                                                          storage_nicname1 = storage_nicname1,
                                                                          storage_nicname2 = storage_nicname2,
                                                                          storage_ip = storage_ip,
                                                                          storage_netmask = storage_netmask,
                                                                          ceph_deploy_ip = ceph_deploy_ip,
                                                                          ceph_members = ceph_members,
                                                                          ceph_mon_members = ceph_mon_members,
                                                                          ceph_osd_members = ceph_osd_members
                                                                        ))
            else:
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_mitaka.ini').render(openstack_version=openstack_version, ha_enable = ha_enable,bond_enable=bond_enable,role_type=role_type,enable_services=enable_services,manage_ip=manage_ip,storage_ip=storage_ip,upstream_internal_ip=upstream_internal_ip))
    else:
        if re.match(r'(^yes|^Yes|^True|^true)',ha_enable) :
            ha_enable = "true"
            if re.match(r'(^yes|^Yes|^True|^true)',bond_enable) :
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_ocata.ini').render(openstack_version=openstack_version, ha_enable = ha_enable,bond_enable=bond_enable,bond_mode=bond_mode,role_type=role_type,enable_services=enable_services,manage_ip=manage_ip,storage_ip=storage_ip,upstream_internal_ip=upstream_internal_ip,controller_internal_members=controller_internal_members,controller_internal_vip=controller_internal_vip))
            else:
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_ocata.ini').render(openstack_version=openstack_version, ha_enable = ha_enable,bond_enable=bond_enable,role_type=role_type,enable_services=enable_services,manage_ip=manage_ip,storage_ip=storage_ip,upstream_internal_ip=upstream_internal_ip,controller_internal_members=controller_internal_members,controller_internal_vip=controller_internal_vip))
        else:
            ha_enable = "false"
            if re.match(r'(^yes|^Yes|^True|^true)',bond_enable) :
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_ocata.ini').render(openstack_version=openstack_version, ha_enable = ha_enable,bond_enable=bond_enable,role_type=role_type,enable_services=enable_services,manage_ip=manage_ip,storage_ip=storage_ip,upstream_internal_ip=upstream_internal_ip))
            else:
                with open(os.path.join(rc_path, "rc_" + manage_ip + ".ini"), 'w') as f:
                    f.write(j2_env.get_template('rc_ocata.ini').render(openstack_version=openstack_version, ha_enable = ha_enable,bond_enable=bond_enable,role_type=role_type,enable_services=enable_services,manage_ip=manage_ip,storage_ip=storage_ip,upstream_internal_ip=upstream_internal_ip))