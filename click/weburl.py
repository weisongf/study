#! /usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser
import time

print("start" + time.ctime())
count = 0;
firefoxPath = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
webbrowser.register('Firefox',None,webbrowser.BackgroundBrowser(firefoxPath))
webbrowser.get('Firefox').open('www.baidu.com',new = 1, autoraise = True)
while (count < 3):
    time.sleep(5)
    #webbrowser.open("http://blog.csdn.net/ko_tin/article/details/72466012")
    #webbrowser.Chrome.open("http://blog.csdn.net/ko_tin/article/details/72466012")
    webbrowser.get('Firefox').open_new_tab('http://edu.inspur.com/login.htm?fromurl=%2fsty%2findex.htm')
    count = count + 1



# chromePath = r'你的浏览器目录'            #  例如我的：C:\***\***\***\***\Google\Chrome\Application\chrome.exe
# webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))  #这里的'chrome'可以用其它任意名字，如chrome111，这里将想打开的浏览器保存到'chrome'
# webbrowser.get('chrome').open('www.baidu.com'，new=1,autoraise=True)