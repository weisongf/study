#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rados
import rbd

cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')


def create_rbd(pool,size,rbd_name):
    try:
        cluster.connect()
        ioctx = cluster.open_ioctx(pool)
        try:
            rbd_inst = rbd.RBD()
            #size:GB
            size = size * 1024**3
            rbd_inst.create(ioctx, rbd_name, size)
            print("Create rbd image:%s" % rbd_name )
            # image = rbd.Image(ioctx, 'myimage')
            # try:
            #     data = 'foo' * 200
            #     image.write(data, 0)
            # finally:
            #     image.close()
        finally:
            ioctx.close()
    finally:
        cluster.shutdown()

def create_snapshot(pool,volume_name,snap_name):
    try:
        cluster.connect()
        ioctx = cluster.open_ioctx(pool)
        try:
            image = rbd.Image(ioctx, volume_name)
            image.create_snap(snap_name)
        #except rados.Error:
        except rbd.ImageExists:
            print("The name already exists")
        finally:
            ioctx.close()
    finally:
        cluster.shutdown()

def remove_snapshot(pool,volume_name,snap_name):
    try:
        cluster.connect()
        ioctx = cluster.open_ioctx(pool)
        try:
            image = rbd.Image(ioctx, volume_name)
            image.remove_snap(snap_name)
        #except rados.Error:
        except rbd.ImageNotFound:
            print("The  ImageNotFound:%s" %snap_name)
        finally:
            ioctx.close()
    finally:
        cluster.shutdown()


def revert_snapshot(pool,volume_name,snap_name):
    # try:
    #     cluster.connect()
    #     ioctx = cluster.open_ioctx(pool)
    #     try:
    #         image = rbd.Image(ioctx, volume_name)
    #         image.rollback_to_snap(snap_name)
    #         print("The rbd snapshot rollback successful")
    #     #except rados.Error:
    #     except rbd.ImageNotFound:
    #         print("The rbd snapshot ImageNotFound")
    #     finally:
    #         ioctx.close()
    # finally:
    #     cluster.shutdown()
    with cluster.connect() as connect:
        with cluster.open_ioctx(pool) as ioctx:
            image = rbd.Image(ioctx, volume_name)
            image.rollback_to_snap(snap_name)
            print("The rbd snapshot rollback successful")



def main():

    #create_snapshot("volumes","myimage","snap2")
    try:
        revert_snapshot("volumes", "myimage", "snap2")
    except rados.Error:
        pass
    remove_snapshot("volumes", "myimage", "snap1")


if __name__ == '__main__':
    main()