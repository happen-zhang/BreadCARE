#-*- coding: UTF-8 -*-

from handlers.base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html', title = '首页', user=self.current_user)
