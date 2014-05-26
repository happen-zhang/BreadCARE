from handlers.base import BaseHandler

class FooHandler(BaseHandler):
    def get(self):
        self.render('foo/index.html')
