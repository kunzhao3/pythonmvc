from flask import session

from goods.common import utils
from goods.config.logConfig import web_log
from goods.entity.user import User
from goods.libs.html import Html
from goods.libs.result import Result


class login:
    @web_log(log_request=True, log_response=True)
    def login(self):
        if utils.isPost():
            param_data = utils.postRequestJson()
            username = param_data.get('username')
            password = param_data.get('password')
            user = User.get_by_username(username)

            if user and User.verify_password(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                data = {
                    "redirect_url": '/system/cart/view_cart'
                }
                return Result.success(msg='登录成功！', data=data)
            else:
                return Result.error(code=1004, msg='用户名或密码错误')
        else:
            return Html.render('/login.html')
    def logout(self):
        if 'user_id' in session:
          session.clear()
        return Html.redirect('/content/login/login')