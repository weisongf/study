#!/usr/bin/python
# -*-coding:utf-8-*-

import yaml

with open("body.yml",'r+') as load_f:
    load_dict = yaml.load(load_f)

print(load_dict)
