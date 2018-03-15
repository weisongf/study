#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

for line in urllib2.urlopen('http://docs.pythontab.com/python/python2.7/stdlib.html#tut-internet-access'):
    line = line.decode('utf-8')
    print line
