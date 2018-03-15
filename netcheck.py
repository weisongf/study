#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os,sys,re
import subprocess

def NetCheck(ip):
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

ip1="172.23.30.2"
domain1="www.bb.com"
NetCheck(ip1)
NetCheck(domain1)