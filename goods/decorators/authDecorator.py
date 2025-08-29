from functools import wraps
from flask import session, flash, redirect

def login_required(f):
    """
    登录验证装饰器
    如果用户未登录，则重定向到登录页面并提示信息。
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录以继续。', 'danger')
            return redirect('/content/login/login')
        return f(*args, **kwargs)
    return decorated_function
