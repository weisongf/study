#! /usr/bin/env python
# -*- coding: utf-8 -*-

class SnapCreateManage(object):
    def __init__(self,params):
        super(SnapCreateManage, self).__init__()
        self.pools = params.get("poolname")
        self.rbdname = params.get("rbdname")
        self.snapname = params.get("snapname")
        self.taskid = params.get("taskid","0")

    def _snap_create(self,params):

        print self.taskid

params = {"poolname":"vms","rbdname":"","snapname":"snap1","taskid":"ok"}
snap_api = SnapCreateManage(params)

snap_api._snap_create(params)