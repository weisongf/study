#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

#r = requests.get(url='http://www.baidu.com')  # 最基本的GET请求
# r = requests.get('https://github.com/timeline.json')
# print(r.status_code)
# print(r.text)
# print(r.headers)


# a = [("a","100")]
#
# print dict(a)
#server_id = ["aaa","bbb","ccc"]
# for i in server_id:
#     payload = {'key1': 'value1', 'key2': i}
#     print payload
#     rg = requests.get('http://httpbin.org/get', params=payload)
#     #rp = requests.post("http://httpbin.org/post", data=payload)
#     rp = requests.post("http://httpbin.org/post", data=json.dumps(payload))
#
#     print rg.url
#     #print rp.text
#     print ("rp.json:",rp.json())
#     print(rp.status_code)
#     print(rp.status_code == requests.codes.ok)


#request 返回数据
name = "test"
# body = {
#     "auth": {
#         "identity": {
#             "methods": [
#                 "password"
#             ],
#             "password": {
#                 "user": {
#                     "name": name,
#                     "domain": {
#                         "name": "Default"
#                     },
#                     "password": "Changeme_123"
#                 }
#             }
#         }
#     }
# }
# try:
#     rp = requests.post('http://172.23.4.81:5000/v3/auth/tokens',json=body,timeout=10)
#     print(rp.status_code)
#     print(rp.text)
# except requests.exceptions.ConnectTimeout:
#     print("ConnectTimeout")
# rp = requests.post('http://172.23.5.81:5000/v3/auth/tokens',json=body,timeout=10)
# create
body = \
    {
            "poolname":"vms",
            "rbdname":"sw3a104f-d36d-4b14-8dc9-ae407881960e_disk",
            "snapname":"snap1534",
            "snapremark":"新年快乐",
            "taskid":"0"
    }
#delete
body_delete = \
{
        "poolname":"vms",
        "rbdname":"sw3a104f-d36d-4b14-8dc9-ae407881960e_disk",
        "snapid":"sw3a104f-d36d-4b14-8dc9-ae407881960e_disk20180223173910"
}
#rp_del = requests.post('http://172.23.30.40:9991/v1/deletesnapshot',json=body_delete,timeout=10)
rp_del = requests.post('http://172.23.60.12:9991/v1/deletesnapshot',json=body_delete,timeout=10)
# rp = requests.post('http://172.23.27.31:8888/snap/createsnap',json=body,timeout=10)
#print(rp_del.content.encode('utf-8'))
rs_dic = dict()
print(rp_del.encoding)
print(rp_del.content)
print(rp_del.text.encode())
print(rp_del.json())
rs_json = rp_del.json()
#msg = rs_json.get('msg')
#rs_dic = json.dumps(rs_json)
#rs_dic['msg'] = '失败'.decode(encoding='utf-8')
rs_dic=json.loads(rp_del.content)
rs_new = json.dumps(rs_dic,ensure_ascii=False)
print(rs_new)
#print(msg)
#print(rp_del.status_code)
