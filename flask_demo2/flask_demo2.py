#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,url_for,redirect
import config
app = Flask(__name__)
app.config.from_object(config)

@app.route('/<user>')
def hello_world(user):
    #1 / 0
    #return 'Hello %s !' % user
    return 'Hello {} !'.format(user)
@app.route('/url')
def url():
    #return url_for('index')
    return url_for('hello_world',user = "Huahua")

@app.route('/index')
def index():
    return "首页测试"

@app.route('/link')
def link():
    return '<a href="%s"> 首页</a>' % url_for('index')

@app.route('/redirect')
def redirect_url():
    return redirect('/index')

if __name__ == '__main__':
    app.run()
