#! /usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce
import pdb

def str2num(s):
    if '.' in s:
        return float(s)
    else:
        return int(s)

def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)

def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    #pdb.set_trace()
    print('99 + 88 + 7.6 =', r)
    str = "今天天气很好"
    #print(str.encode('utf-8'))
    print(str)

main()