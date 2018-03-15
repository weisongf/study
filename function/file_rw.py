#! /usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
# hosts_openstack_82_new='C:\Users\song.w\PycharmProjects\study\/function\hosts_openstack_82_new'
# hosts_openstack_82='C:\Users\song.w\PycharmProjects\study\/function\hosts_openstack_82'
# with open(hosts_openstack_82_new, 'w') as f:
#     f.write(''.join([line for line in open(hosts_openstack_82).readlines() if '172.23.30.60' not in line]))
#
# shutil.move(hosts_openstack_82, hosts_openstack_82 + '_bak')
# shutil.move(hosts_openstack_82_new, hosts_openstack_82)

hosts_manageip = {'add2':'172.23.30.59',"add1":'172.23.30.61'}

env_manageips_file_new='C:\Users\song.w\PycharmProjects\study\/function\hosts_openstack_82_new'
env_manageips_file='C:\Users\song.w\PycharmProjects\study\/function\hosts_openstack_82'

for k in sorted(hosts_manageip):
    print sorted(hosts_manageip)
    with open(env_manageips_file, 'r') as f_env:
        with open(env_manageips_file_new, 'w') as f:
            print f_env.readlines()
            for line in f_env.readlines():
                print line
                if hosts_manageip[k] not in line:
                    print hosts_manageip[k]
                    f.write(line)

    shutil.move(env_manageips_file, env_manageips_file + '_bak')
    shutil.move(env_manageips_file_new, env_manageips_file)

with open(env_manageips_file, 'a') as f:
    for k in sorted(hosts_manageip):
        print hosts_manageip[k]
        f.write(hosts_manageip[k] + ' ' + k + '\n')

################
    # for k in sorted(hosts_manageip):
    #     with open(env_manageips_file, 'r') as f_env:
    #         with open(env_manageips_file_new, 'w') as f:
    #             for line in f_env.readlines():
    #                 if hosts_manageip[k] not in line:
    #                     f.write(line)
    #     shutil.move(env_manageips_file, env_manageips_file + '_bak')
    #     shutil.move(env_manageips_file_new, env_manageips_file)
    #
    # with open(env_manageips_file, 'a') as f_env:
    #
    #     for k in sorted(hosts_manageip):
    #         f_env.write(hosts_manageip[k] + ' ' + k + '\n')