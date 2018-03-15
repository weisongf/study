#! /usr/bin/env python
# -*- coding: utf-8 -*-

with open("aa.txt","r") as reader, open("bb.txt","w+") as writer:
    writer.write(reader.read())
