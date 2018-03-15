#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

class Error(Exception):
    """Base class for exceptions in this module."""
    msg = ("The program encountered an error.")


class GetConfig:
    def __init__(self,filename):
        self.filename = filename

    def get_config(self):
        config = ConfigParser.ConfigParser()
        config.read(self.filename)
        return config

conf_file = "C:\Users\song.w\PycharmProjects\study\/function\/rc_ceph2.ini"

try:
    conf = GetConfig(conf_file)
    open(conf_file,"r")
except IOError as err:
    print("The file is not exist:")

ins = conf.get_config()
try:
    print ins.get("ceph","ceph_deploy_ip")
except  ConfigParser.NoSectionError:
    print("ConfigParser.NoSectionError: No section: 'ceph'")


