#! /usr/bin/env python
# -*- coding: utf-8 -*-

import usb.core as core
import usb.util as util
import usb.control as control

usb_list={}
usb_attr=["bcdUSB","iManufacturer",'iProduct','idVendor','product','manufacturer']


for dev in core.find(find_all=True):
    #cfg = util.find_descriptor(dev)
    #print cfg
    dev_id = dev._str()
    usb_list[dev_id]={}
    for attr in usb_attr:
        if attr == "bcdUSB":
            if dev.bcdUSB & 0xf:
                low_bcd_usb = str(dev.bcdUSB & 0xf)
            else:
                low_bcd_usb = ""
            usb_list[dev_id]['bcdUSB'] = "%#5x USB %d.%d%s" % (
                     dev.bcdUSB, (dev.bcdUSB & 0xff00)>>8,
                    (dev.bcdUSB & 0xf0) >> 4, low_bcd_usb)

        elif attr == "idProduct":
            usb_list[dev_id][attr] = hex(dev.idProduct)
        elif attr == "idVendor":
            usb_list[dev_id][attr] = hex(dev.idVendor)
        else:
            usb_list[dev_id][attr] = eval("dev."+attr)
    #print dev.iManufacturer,dev.iProduct,hex(dev.idProduct),hex(dev.idVendor),dev.product,dev.manufacturer
    #print control.get_descriptor(dev)
    #print dev.desc
print   usb_list
