from flask import flash

from goods.common import utils
from goods.config.logConfig import web_log
from goods.entity.user import User
from goods.libs.html import Html
from goods.libs.result import Result


class register:
    @web_log(log_request=True, log_response=True)
    def register(self):
        if utils.isPost():
            param_data = utils.postRequestJson()
            username = param_data['username']
            password = param_data['password']

            if User.get_by_username(username):
                return Result.error(code=1004, msg='用户名已存在')

            try:
                User.create(username, password)
                flash('注册成功，请登录', 'success')
                data = {
                    "redirect_url": '/content/login/login'
                }
                return Result.success(msg='注册成功！', data=data)
            except Exception as e:
                return Html.render('/404.html')

        return Html.render('/register.html')

