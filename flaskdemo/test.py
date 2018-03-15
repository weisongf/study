#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/') #路由主页，返回test.html页面
def index():
    return render_template('test.html')

@app.route('/mysql/<arg1>', methods=['GET', 'POST']) #mysql功能路由，带参数的方便，查询，修改，更新，删除功能的实现，这里未连接mysql，采用模拟数据实现
def mysql(arg1):
        data = {'total':2, 'rows':[{'firstname':1, 'lastname':2, 'phone': '3', 'email':'12345@qq.com'},{'firstname':4, 'lastname':5, 'phone': '6', 'email':'12345@qq.com'}]}
        j_reslist = json.dumps(data) #data数据为模拟数据，total为显示的页数，rows为行数，rows中firstname,lastname,phone,email对应为test.html中的参数
        print j_reslist
        return j_reslist

if __name__ == '__main__':
    app.run('0.0.0.0')