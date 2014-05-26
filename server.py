
import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import torndb

from tornado.options import define, options

define('PORT', default = 8888)
define('DB_HOST', default = '127.0.0.1:3306')
define('DB_NAME', default = 'breadcare')
define('DB_USER', default = 'root')
define('DB_PASSWORD', default = 'happen')

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class HomeHandler(BaseHandler):
    def get(self):
        users = self.db.query('SELECT * FROM `user_bc`')

        if not users:
            self.redirect('/error')

        for user in users:
            print user.username

        self.write('Hello World')

class ErrorHandler(BaseHandler):
    def get(self):
        self.render('error.html', title = '500')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/error', ErrorHandler)
        ]

        settings = dict(
            blog_title = u"Can not get a Chinese name?",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = True,
            cookie_secret = "mysecret",
            login_url = "/user/login",
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = torndb.Connection(
            host = options.DB_HOST,
            database = options.DB_NAME,
            user = options.DB_USER,
            password = options.DB_PASSWORD
        )

def bootstrap():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.PORT)
    tornado.ioloop.IOLoop.instance().start()

if '__main__' == __name__:
    bootstrap()
