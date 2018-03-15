#! /usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import json
import datetime

# [mysql]
# host = 10.110.1.26
# username = root
# pwd = 123456a?
# db = icp

# 打开数据库连接
db = MySQLdb.connect("10.110.1.26","root","123456a?","icp",charset = 'utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT * FROM std_ceph_snap Where rbdname = 'sw3a104f-d36d-4b14-8dc9-ae407881960e_disk'")

# 使用 fetchone() 方法获取一条数据
# 使用 fetchall() 方法获取所有数据
data = cursor.fetchall()

print(data)
#关闭游标
cursor.close()
# 关闭数据库连接
db.close()

jsonData = []

for row in data:
    result = {}
    result['id'] = row[0]
    result['parentid'] = row[1]
    result['snaporgid'] = row[2]
    result['taskid'] = row[3]
    result['snapname'] = row[4]
    result['size'] = row[5]
    result['status'] = row[6]
    result['active'] = row[7]
    result['poolname'] = row[8]
    result['rbdname'] = row[9]
    result['starttime'] = row[10].strftime( '%Y-%m-%d %H:%M:%S %f' )
    result['endtime'] = row[11].strftime( '%Y-%m-%d %H:%M:%S %f' )
    result['remark'] = row[12]
    jsonData.append(result)
    print u'转换为列表字典的原始数据：', jsonData

jsondatar = json.dumps(jsonData,ensure_ascii=False)
print("jsondatar=",jsondatar)
