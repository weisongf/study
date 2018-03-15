#!/usr/bin/env python

################################################################################
# NOTICE:
# This file is added to implement an agent on server side to collect configuration
# and running status information, report information to iddm server and perform 
# heartbeat with iddm server.
#
# AUTHOR: HU-Zhangfeng, Jiang-Fangwen
# AFFILIATION: INSPUR
# DATE: 2017/08/01
################################################################################

import ConfigParser
from iddm.utils import write_pidfile
from socket import socket, AF_INET, AF_UNIX, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import time
import threading
import commands
import simplejson

config = ConfigParser.ConfigParser()
config.read("/etc/iddm/iddm.cfg")

# fill common parameters
MY_PATH = config.get("common", "my_path")
PID_FILE_PATH = config.get("common", "pid_file_path")
IDDM_SERVER_IP = config.get("common", "iddm_server_ip")
IDDM_SERVER_PORT = int(config.get("common", "iddm_server_port"))
IDDM_HEARTBEAT_PORT = int(config.get("common", "iddm_heartbeat_port"))
IDDM_HEARTBEAT_INTERVAL = int(config.get("common", "iddm_heartbeat_interval"))
IDDM_REPORT_INTERVAL = int(config.get("common", "iddm_report_interval"))



class Agent():
    __doc__ = "This is IDDM Agent!"

    # constructor
    def __init__(self,):
        self.report_address = (IDDM_SERVER_IP, IDDM_SERVER_PORT)
        self.heartbeat_address = (IDDM_SERVER_IP, IDDM_HEARTBEAT_PORT)
        self.heartbeat_sock = socket(AF_INET, SOCK_DGRAM)
        self.hb = self.make_heartbeat()


    # prepare the heartbeat info
    def make_heartbeat(self,):
        hb = {}
        val, result = commands.getstatusoutput('lldpcli show chassis')
        if val != 0:
            return None
        res_list = result.split('\n')
        for tmp in res_list:
            tmp_lower = tmp.lower()
            
            # fill chassisid
            if 'chassisid' in tmp_lower:
                hb['chassisid'] = tmp.strip(' ').split(' ')[-1].strip(' ')
                
            # fill sysname
            if 'sysname' in tmp_lower:
                hb['sysname'] = tmp.strip(' ').split(' ')[-1].strip(' ')
                
            # fill sysdescr
            if 'sysdescr' in tmp_lower:
                hb['sysdescr'] = tmp[tmp.index(':')+1:].strip(' ')

            # fill mgmtip
            if 'mgmtip' in tmp_lower:
                mgmtip = tmp[tmp.index(':')+1:].strip(' ')
                if len(mgmtip) < 20:
                    hb['mgmtip4'] = mgmtip
                else:
                    hb['mgmtip6'] = mgmtip

        # return a valid hb
        if len(hb.keys()) != 5:
            return None
        return hb
        

    # send heart beat to IDDM server
    def send_heartbeat(self, hb):
        # hb is none
        if not hb:
            return

        # send heartbeat through udp
        msg = simplejson.dumps(hb)
        print "hb====%s===="%(msg,)
        self.heartbeat_sock.sendto(msg, self.heartbeat_address) 
        return


    # prepare the report info
    def make_report(self,):
        rp = {}

        # fill basic info
        val, result = commands.getstatusoutput('lldpcli show chassis')
        if val != 0:
            return None
        res_list = result.split('\n')
        for tmp in res_list:
            tmp_lower = tmp.lower()
            
            # fill chassisid
            if 'chassisid' in tmp_lower:
                rp['chassisid'] = tmp.strip(' ').split(' ')[-1].strip(' ')
                
            # fill sysname
            if 'sysname' in tmp_lower:
                rp['sysname'] = tmp.strip(' ').split(' ')[-1].strip(' ')
                
            # fill sysdescr
            if 'sysdescr' in tmp_lower:
                rp['sysdescr'] = tmp[tmp.index(':')+1:].strip(' ')

            # fill mgmtip
            if 'mgmtip' in tmp_lower:
                mgmtip = tmp[tmp.index(':')+1:].strip(' ')
                if len(mgmtip) < 20:
                    rp['mgmtip4'] = mgmtip
                else:
                    rp['mgmtip6'] = mgmtip

        # get cpu flag
        val, result = commands.getstatusoutput('lscpu')
        if val != 0:
            return None
        res_list = result.split('\n')
        architecture =''
        for tmp in res_list:
            if 'Architecture:' in tmp:
                architecture = tmp.strip(' ').split(':')[-1].strip(' ')
                break

        # get cpu architecture
        val, result = commands.getstatusoutput('cat /proc/cpuinfo')
        if val != 0:
            return None
        res_list = result.split('\n')
        flags =''
        for tmp in res_list:
            if 'flags' in tmp:
                flags = tmp.strip(' ').split(':')[-1].strip(' ')
                break

        # fill cpu info
        val, result = commands.getstatusoutput('dmidecode --type processor')
        if val != 0:
            return None
        res_list = result.split('\n')
        rp['cpuinfo'] = []
        cpuinfo = {}
        for tmp in res_list:
            if 'Socket Designation:' in tmp:
                cpuinfo['cpuid'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Type:' in tmp:
                if not cpuinfo or 'cpuid' not in cpuinfo:
                    break
                cpuinfo['type'] = tmp.strip(' ').split(':')[-1].strip(' ')
                
            if 'Family:' in tmp:
                if not cpuinfo or 'type' not in cpuinfo:
                    break
                cpuinfo['family'] = tmp.strip(' ').split(':')[-1].strip(' ')
                
            if 'Manufacturer:' in tmp:
                if not cpuinfo or 'family' not in cpuinfo:
                    break
                cpuinfo['vendor'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Version:' in tmp:
                if not cpuinfo or 'vendor' not in cpuinfo:
                    break
                cpuinfo['model_name'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Max Speed:' in tmp:
                if not cpuinfo or 'model_name' not in cpuinfo:
                    break
                cpuinfo['maxspeed'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Current Speed:' in tmp:
                if not cpuinfo or 'maxspeed' not in cpuinfo:
                    break
                cpuinfo['curspeed'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Core Count:' in tmp:
                if not cpuinfo or 'curspeed' not in cpuinfo:
                    break
                cpuinfo['corenum'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Thread Count:' in tmp:
                if not cpuinfo or 'corenum' not in cpuinfo:
                    break
                cpuinfo['threadnum'] = tmp.strip(' ').split(':')[-1].strip(' ')
                cpuinfo['architecture'] = architecture
                cpuinfo['flags'] = flags
                rp['cpuinfo'].append(cpuinfo)
                cpuinfo = {}

        # fill memory info
        val, result = commands.getstatusoutput('dmidecode --type memory')
        if val != 0:
            return None
        res_list = result.split('\n')
        rp['meminfo'] = []
        meminfo = {}
        for tmp in res_list:
            if 'Size:' in tmp and 'MB' in tmp:
                size = 1024*1024*int(tmp.strip(' ').split(':')[-1].strip(' ').split(' ')[0].strip(' '))
                meminfo['size'] = size

            if 'Locator:' in tmp:
                if 'size' not in meminfo:
                    break
                meminfo['memid'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Type:' in tmp and 'Error Correction Type:' not in tmp:
                if 'memid' not in meminfo:
                    break
                meminfo['type'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Speed:' in tmp:
                if 'type' not in meminfo:
                    break
                meminfo['speed'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Manufacturer:' in tmp:
                if 'speed' not in meminfo:
                    break
                meminfo['vendor'] = tmp.strip(' ').split(':')[-1].strip(' ')

            if 'Serial Number:' in tmp:
                if 'vendor' not in meminfo:
                    break
                meminfo['serialnum'] = tmp.strip(' ').split(':')[-1].strip(' ')
                rp['meminfo'].append(meminfo)
                meminfo = {}


        # fill disk info
        val, result = commands.getstatusoutput('lsblk -Pbdi')
        if val != 0:
            return None
        res_list = result.split('\n')
        rp['diskinfo'] = []
        diskinfo = {}
        for tmp in res_list:
            if 'disk' in tmp:
                diskinfo = {}
                diskinfo['diskid'] = tmp.split(' ')[0].split('\"')[1].strip(' ')
                diskinfo['size'] = int(tmp.split(' ')[3].split('\"')[1].strip(' '))
                diskinfo['rotational'] = int(tmp.split(' ')[4].split('\"')[1].strip(' '))
                rp['diskinfo'].append(diskinfo)

        # fill nic info
        val, result = commands.getstatusoutput('ip link show')
        if val != 0:
            return None
        res_list = result.split('\n')
        rp['nicinfo'] = []
        nicinfo = {}
        for tmp in res_list:
            nicinfo = {}
            if '<' in tmp:
                nicinfo['nicid'] = tmp.split(':')[1].strip(' ')
                nicinfo['nicalias'] = tmp.split(':')[0].strip(' ')
                k, v = commands.getstatusoutput('ethtool %s'%(nicinfo['nicid'],))
                if k != 0:
                    continue
                for t in v.split('\n'):
                    if 'Speed:' in t:
                        nicinfo['speed'] = t.split(':')[-1].split('M')[0].strip(' ')
                # not a physical nic
                if 'speed' not in nicinfo:
                    continue

                p, q = commands.getstatusoutput('ip link show %s'%(nicinfo['nicid'],))
                if p != 0:
                    return None
                for m in q.split('\n'):
                    if 'link/ether' in m:
                        nicinfo['macaddr'] = m.strip(' ').split(' ')[1].strip(' ')
                if 'macaddr' not in nicinfo:
                    continue
                rp['nicinfo'].append(nicinfo)
                    
        return rp


    # report server info to IDDM server
    def send_report(self, rp):
        # rp is none
        if not rp:
            return
            
        # connect to iddm server
        msg = simplejson.dumps(rp)
        print "rp====%s===="%(msg,)
        report_sock = socket(AF_INET, SOCK_STREAM)
        report_sock.connect(self.report_address)
        report_sock.send(msg)
        report_sock.send('==end')
        report_sock.close()
        return


# main thread of IDDM Agent
def main():

    my_agent = Agent()
    
    hb_time = rp_time = time.time()

    # main loop
    while True:

        # send heart beat to IDDM server every 10s
        if (time.time() - hb_time) > IDDM_HEARTBEAT_INTERVAL:
            my_agent.send_heartbeat(my_agent.hb)
            hb_time = time.time()

        # report server info to IDDM server every 30s
        if (time.time() - rp_time) > IDDM_REPORT_INTERVAL:
            rp = my_agent.make_report()
            my_agent.send_report(rp)
            rp_time = time.time()

        time.sleep(1)
    

if __name__ == "__main__":

    main()




