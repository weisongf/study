#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rados
import rbd


def rbd_proxy(ceph_conffile, pools):
    with rados.Rados(conffile=ceph_conffile) as cluster:
        with cluster.open_ioctx(pools) as ioctx:
            rbd_inst = rbd.RBD()
            # size = 4 * 1024**3  # 4 GiB
            # rbd_inst.create(ioctx, 'myimage', size)
            # rbd_list = rbd_inst.list(ioctx)
            # print("rbd_list:%s" % rbd_list)
            # with rbd.Image(ioctx, 'myimage') as image:
            #     data = 'foo' * 200
            #     image.write(data, 0)
            rbd_list(rbd_inst, ioctx)
            # return rbd_inst,ioctx
def rbd_create(ceph_conffile, pools,size,volume):
    with rados.Rados(conffile=ceph_conffile) as cluster:
        with cluster.open_ioctx(pools) as ioctx:
            rbd_inst = rbd.RBD()
            size = size * 1024**3  # 4 GiB
            try:
                 rbd_inst.create(ioctx, volume, size)
            except rbd.ImageExists:
                print("rbd ImageExists")
            except TypeError:
                print("rbd TypeError")
            except rbd.InvalidArgument:
                print("rbd create InvalidArgument")

def rbd_remove(ceph_conffile, pools,volume):
    with rados.Rados(conffile=ceph_conffile) as cluster:
        with cluster.open_ioctx(pools) as ioctx:
            rbd_inst = rbd.RBD()
            rbd_inst.remove(ioctx, volume)
            print("The volume:%s to removed" % volume)

def rbd_snap(ceph_conffile, pools,volume,snapname):
    with rados.Rados(conffile=ceph_conffile) as cluster:
        with cluster.open_ioctx(pools) as ioctx:
            with rbd.Image(ioctx, volume) as image:
                image.create_snap(snapname)

def rbd_rollback(ceph_conffile, pools,volume,snapname):
    with rados.Rados(conffile=ceph_conffile) as cluster:
        with cluster.open_ioctx(pools) as ioctx:
            with rbd.Image(ioctx, volume) as image:
                try:
                    image.rollback_to_snap(snapname)
                    print("The volume:%s to revert snapshot:%s" %(volume,snapname))
                except rbd.ImageNotFound:
                    print("rbd snapshot NotFound")

def rbd_list(rbd_inst, ioctx):
    # cluster,rbd_instance,ioctx =  rbd_proxy(ceph_conffile,pools)

    rbd_ls = rbd_inst.list(ioctx)
    print  rbd_ls
    # print rbd_instance,ioctx


def main():
    ceph_conffile = "/etc/ceph/ceph.conf"
    pools = "volumes"
    # rbd_list(ceph_conffile,pools)
    #rbd_proxy(ceph_conffile, pools)
    #rbd_snap(ceph_conffile, pools, "myimage", "snap01")
    rbd_create(ceph_conffile, pools, 0, "swimage")
    #rbd_remove(ceph_conffile, pools, "swimage")
    #rbd_rollback(ceph_conffile, pools, "myimage", "snap01")


if __name__ == '__main__':
    main()

