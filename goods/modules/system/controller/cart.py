from flask import session,flash

from goods.common import utils
from goods.entity.cartItem import CartItem
from goods.entity.product import Product
from goods.libs.html import Html


class cart:
    def add_to_cart(self):
        try:
            param_data = utils.getRequestJson()
            product_id = param_data['product_id']
            product = Product.get_by_id(product_id)
            if not product:
                return Html.redirect('/content/products/init')
            else:
                CartItem.add_item(session['user_id'],product_id)
                flash('商品已加入购物车', 'success')
                return Html.redirect('/content/products/init')
        except Exception as e:
            flash('添加商品失败', 'danger')
            return Html.render("/404.html")

    def view_cart(self):
        try:
            cart_items = CartItem.get_user_cart(session['user_id'])
            total = sum(item['price'] * item['quantity'] for item in cart_items)
            return Html.render('/cart.html', cart_items=cart_items, total=total)
        except Exception as e:
            return Html.render("/404.html")

    def update_cart(self):
        try:
            request_data = utils.getRequestJson()
            from_data = utils.postRequestByForm()
            new_quantity = int(from_data['quantity'])
            if new_quantity < 1:
                raise ValueError("数量不能小于1")
            else:
                CartItem.update_quantity(request_data['item_id'], session['user_id'], new_quantity)
        except ValueError as e:
            return Html.render("/404.html")
        except Exception as e:
            return Html.render("/404.html")

        return Html.redirect('/system/cart/view_cart')
   
    def remove_from_cart(self):
        try:
            param_data = utils.getRequestJson()
            CartItem.remove_item(param_data['item_id'], session['user_id'])
        except Exception as e:
            return Html.render("/404.html")

        return Html.redirect('/system/cart/view_cart')

    def checkout(self):
        cart_items = CartItem.get_user_cart(session['user_id'])
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        return Html.render('/checkout.html', cart_items=cart_items, total=total)

    def order_confirmation(self):
        # 清空购物车
        CartItem.clear_cart(session['user_id'])
        return Html.render('/order_confirmation.html')