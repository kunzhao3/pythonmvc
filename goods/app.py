import os

from flask import Flask, render_template, redirect, url_for, request, session, flash
from goods.config.config import  Configure
import logging

from goods.decorators.authDecorator import login_required
from goods.entity.cartItem import CartItem
from goods.entity.product import Product
from goods.entity.user import User
from goods.libs.result import Result

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

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return redirect(url_for('product_list'))

@app.route('/content/login/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.get_json().get('username')
        password = request.get_json().get('password')
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
    return render_template('login.html')

@app.route('/content/register/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.get_json().get('username')
        password = request.get_json().get('password')

        if User.get_by_username(username):
            flash('用户名已存在', 'danger')
            return Result.error(code=1004, msg='用户名已存在')

        try:
            User.create(username, password)
            flash('注册成功，请登录', 'success')
            data = {
                "redirect_url": '/content/login/login'
            }
            return Result.success(msg='注册成功！', data=data)
        except Exception as e:
            logger.error(f"注册失败: {str(e)}")
            flash('注册失败，请重试', 'danger')
    return render_template('register.html')

@app.route('/content/products/init')
def product_list():
    try:
        products = Product.get_all()
        return render_template('products.html', products=products)
    except Exception as e:
        logger.error(f"获取商品失败: {str(e)}")
        flash('获取商品信息失败', 'danger')
        return redirect(url_for('index'))

@app.route('/system/cart/view_cart')
@login_required
def view_cart():
    try:
        cart_items = CartItem.get_user_cart(session['user_id'])
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, total=total)
    except Exception as e:
        logger.error(f"获取购物车失败: {str(e)}")
        flash('获取购物车信息失败', 'danger')
        return redirect(url_for('product_list'))

@app.route('/system/cart/add_to_cart')
@login_required
def add_to_cart():
    try:
        product_id = request.args.get('product_id')
        product = Product.get_by_id(product_id)
        if not product:
            flash('商品不存在', 'danger')
            return redirect(url_for('product_list'))

        CartItem.add_item(session['user_id'], product_id)
        flash('商品已加入购物车', 'success')
    except Exception as e:
        logger.error(f"添加失败: {str(e)}")
        flash('添加商品失败', 'danger')
    return redirect(url_for('product_list'))

@app.route('/system/cart/update_cart', methods=['POST'])
@login_required
def update_cart():
    try:
        item_id = request.args.get('item_id')
        new_quantity = int(request.form.get('quantity', 1))
        if new_quantity < 1:
            raise ValueError("数量不能小于1")

        CartItem.update_quantity(item_id, session['user_id'], new_quantity)
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        logger.error(f"更新失败: {str(e)}")
        flash('更新数量失败', 'danger')
    return redirect(url_for('view_cart'))

@app.route('/system/cart/remove_from_cart')
@login_required
def remove_from_cart():
    try:
        item_id = request.args.get('item_id')
        CartItem.remove_item(item_id, session['user_id'])
    except Exception as e:
        logger.error(f"移除失败: {str(e)}")
        flash('移除商品失败', 'danger')
    return redirect(url_for('view_cart'))
# app.py 路由部分
@app.route('/system/cart/checkout')
@login_required
def checkout():
    """展示结算页面"""
    cart_items = CartItem.get_user_cart(session['user_id'])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/system/cart/order_confirmation')
@login_required
def order_confirmation():
    """展示订单确认页面"""
    # 清空购物车
    CartItem.clear_cart(session['user_id'])
    return render_template('order_confirmation.html')
@app.route('/content/login/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(
        host = app.config['server']['host'],
        port = app.config['server']['port'],
        debug = app.config['server']['debug']
    )