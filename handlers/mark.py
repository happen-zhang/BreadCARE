#-*- coding: UTF-8 -*-
from handlers.base import BaseHandler

class MarkHandler(BaseHandler):
    def get(self, username):
        user = self.wdb().get( "SELECT * FROM user WHERE username='%s'" % username )
        try:
            user.uid
        except Exception, e:
            self.render( 'message.html', title = "提示", message = "尝试请求的用户不存在", user=self.current_user )

        try:
            self.current_user[ 'uid' ]
        except Exception, e:
            self.current_user[ 'uid' ] = 0
            self.render( 'message.html', title = "提示", message = "尝试请求的用户没有公开的书签，您可以看看别人的书签", user=self.current_user )
        if self.current_user[ 'uid' ] == str(user.uid):
            # 是同一个用户
            my_marks = self.rdb().query( "SELECT * FROM mark WHERE uid=%d" % user.uid )
        else:
            my_marks = self.rdb().query( "SELECT * FROM mark WHERE uid=%d and ispublic=1" )
        self.render('my_bookmarks.html', title = username + u"的书签", user = self.current_user, my_marks = my_marks )
