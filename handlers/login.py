#-*- coding: UTF-8 -*-

from handlers.base import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html', title = '登陆', user = self.current_user)

    def post(self):
        try:
            email = self.get_argument( 'email' )
            password = self.get_argument( 'password' )
        except Exception, e:
            self.render( 'login.html', title = '登陆' , message = "您提交的参数不足", user=self.current_user)

        user = self.rdb().get( "SELECT * FROM user WHERE email=%s" , email)
        try:
        	user.username
        except Exception, e:
        	self.render( 'login.html', title = '登陆', message = '账号不存在', user=self.current_user)

        import md5
        key = md5.new()
        key.update( password + user.salt )
        md5password = key.hexdigest()
        if user.password == md5password:
            # login success
            user_data = {
                "uid" : str(user.uid),
                "name" : user.username,
                "email" : user.email
            }
            self.set_secure_cookie( 'user_data' , str(user_data) ) # 可以用 dict() 转换回来
            self.render( 'index.html', title = "首页", user = user_data)
        else:
            self.render( 'login.html', title = '登陆', message = '密码错误', user=self.current_user)