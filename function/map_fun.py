#! /usr/bin/env python
# -*- coding: utf-8 -*-

items = [1, 2, 3, 4, 5]
squared = []
for i in items:
    squared.append(i**2)

print squared

sqr_list = list(map(lambda x:x**2,items))
print sqr_list


#filter

filter_list = list(filter(lambda i:i>3,items))
print filter_list


