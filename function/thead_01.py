#! /usr/bin/env python
# -*- coding: utf-8 -*-

import thread
import time

# define a thread function

def print_time(threadName,delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count +=1
        print "%s: %s" % ( threadName, time.ctime(time.time()) )



# 创建两个线程
try:
    thread.start_new_thread(print_time, ("Thread-1", 2,))
    thread.start_new_thread(print_time, ("Thread-2", 4,))
except:
    print "Error: unable to start thread"
    msg = ("Please check thread program")
    raise

while 1:
    pass
