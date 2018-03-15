#! /usr/bin/env python
# -*- coding: utf-8 -*-

def test_var_args(f_arg, *argv):
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv:", arg)

test_var_args('yasoob', 'python', 'eggs', 'test')

def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} == {1}".format(key, value))
    print kwargs.get("db")

#greet_me(name="song.w",age=33)

kwargs = {"db":"cinder","host":"127.0.0.1","db_user":"cinder","db_passwd":"Changeme_123"}
greet_me(**kwargs)

a_set = {'red', 'blue', 'green'}
b_set = {'red','yellow'}
print(a_set|b_set)


for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print( n, 'equals', x, '*', n/x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')

a , b = 3 , 4
print a,b

#协程

def grep(pattern):
    print("Searching for", pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)


search = grep('coroutine')
next(search)
search.send("I love you")
search.send("Don't you love me?")
search.send("I love coroutine instead!")


