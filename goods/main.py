import os
import re

from flask import Flask, request, session, redirect, flash
from goods.config.config import Configure
from goods.libs.application import Application

@Configure
def create_app(cfg):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
    template_folder_dir = root_dir + '/resources/templates'
    static_folder_dir = root_dir + '/static'
    app = Flask(__name__, template_folder=template_folder_dir,static_folder=static_folder_dir) # 配置 Flask 静态文件路由
    app.secret_key = cfg['token']['secret']
    app.config['server'] = cfg['server']
    app.config['check_login_urls']=cfg['check_login_urls']
    return app

app = create_app()

@app.before_request
def before_request():
    check_login_urls = app.config['check_login_urls']
    path = request.path
    pattern = re.compile('%s' % "|".join(check_login_urls))
    if pattern.match(path):
       # 判断用户是否已经登录
       if 'user_id' not in session:
         flash('请先登录以继续。', 'danger')
         return redirect('/content/login/login')

    return
@app.route('/', defaults={'moduleName': '/','className':'','methodName':''})
@app.route("/<path:moduleName>/<path:className>/<path:methodName>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def index(moduleName,className,methodName):
    method = request.method
    if (method == 'GET' or method == 'POST')  and moduleName!='/':
        return Application.init(moduleName,className,methodName)
    # 产品列表页面 /content/controller/product/init()
    return Application.init('content','products','init')

if __name__ == '__main__':
    app.run(
        host = app.config['server']['host'],
        port = app.config['server']['port'],
        debug = app.config['server']['debug']
    )