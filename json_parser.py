#!/usr/bin/python
# -*-coding:utf-8-*-

import json

with open("json_data02.json",'r+') as load_f:
    load_dict = json.load(load_f)
    print(len(load_dict["nodes"]))
    print(load_dict["nodes"][0])
    print(load_dict["nodes"][1]["network"]["manage_ip"])
    print(load_dict["nodes"][1]["network"]["manage_nicname"])
    print(load_dict["nodes"][1]["role"]["role_type"])

def hjson(load_dict,i=0):
    #print(load_dict)
    if (isinstance(load_dict,dict)):
        for items in load_dict:
            if (isinstance(load_dict[items],dict)):
                print("****"*i+"%s:%s"%(items,load_dict[items]))
            else:
                print("****"*i+"%s:%s"%(items,load_dict[items]))
    else:
        print("load_dict is not json object!")

hjson(load_dict,0)