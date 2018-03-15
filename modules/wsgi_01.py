#! /usr/bin/env python
# -*- coding: utf-8 -*-

#利用wsgiref 作为wsgi server
from wsgiref.simple_server import make_server
"""
def simple_app(environ, start_response):
    status = '200 ok'
    response_headers = [('Content-type', 'text/plain')]     #设置http头
    start_response(status, response_headers)
    return [u"test wsgi app".encode('utf-8')]

class AppClass(object):
    def __call__(self, environ, start_response):
        status = "200 ok"
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [u"class AppClass".encode('utf-8')]
"""

#wsgi app只要是一个callable对象即可，不一定要是函数
#一个实现了__call__方法示例也ok的

#httpd = make_server('', 8080, simple_app)
"""
app = AppClass()
httpd = make_server('', 8080, app)
httpd.serve_forever()
"""
URL_PATTERNS = (
        ('AA/', 'AA_app'),
        ('BB/', 'BB_app'),
        )

class Dispatcher(object):
    #实现路由功能：
    def _match(self, path):
        path = path.split('/')[1]
        for url, app in URL_PATTERNS:
            if path in url:
                return app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        app = self._match(path)
        if app:
            app = globals()[app]
            return app(environ, start_response)
        else:
            start_response("404 NOT FOUND",[('Content-type', 'text/plain')])
            return ["page dose not exists"]

def AA_app(environ, start_response):
    start_response("200 OK",[('Content-type', 'text/html')])
    return ["AA page"]

def BB_app(environ, start_response):
    start_response("200 OK",[('Content-type', 'text/html')])
    return ["BB page"]

app = Dispatcher()
httpd = make_server('', 8090, app)
httpd.serve_forever()

# 测试结果：
# server端：
# root@u163:~/cp163/python# python wsgi_app.py
# 192.168.2.162 - - [04/Nov/2015 18:44:06] "GET /AA HTTP/1.1" 200 7
# 192.168.2.162 - - [04/Nov/2015 18:44:22] "GET /BB HTTP/1.1" 200 7
#
# client端：
# root@u162:~# curl http://192.168.2.163:8090/AA
# AA page
# root@u162:~# curl http://192.168.2.163:8090/BB
# BB page
# root@u162:~#