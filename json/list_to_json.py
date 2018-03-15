#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json

a_list = ["a","b","c"]
#b_dic = [{"id":"a"},{"id":"b"},{"id":"c"}]

result = [{"id":value for value in i} for i in a_list]

print(json.dumps(result))
