#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from settings import settings
from routes import routes

class BreadCARE(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, routes, **settings)

def bootstrap():
    app = BreadCARE()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    bootstrap()
