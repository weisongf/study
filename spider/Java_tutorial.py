#! /usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import re

index_ = requests.get('http://www.runoob.com/java/java-tutorial.html')
contents = index_.content

items = re.findall(r'"href":"(.*?)"', contents)

if len(items) == 0:
        print "The End Page:", page
        data = urllib.urlencode(data) # 编码工作，由dict转为string
        full_url = url+'?'+data
        print full_url
        sys.exit(0) # 无错误退出
    else:
        print "The Page:", page, "Downloading..."
        for item in items:
            ContentSave(item)
#print index_.text