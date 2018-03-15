#!/usr/bin/python
# -*-coding:utf-8-*-

def add(x, *arg):
    print x
    result = x
    print arg
    for i in arg:
        result +=i
    print result

add(1,2,3,4,5,6,7,8,9,10)

def fun1(*args):
    print args
fun1("aa","bb",2,3)






