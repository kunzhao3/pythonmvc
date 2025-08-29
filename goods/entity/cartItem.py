from goods.libs.database import Database


class CartItem:
    """购物车模型"""
    @classmethod
    def add_item(cls, user_id, product_id):
        existing = cls.get_item(user_id, product_id)
        if existing:
            sql = "UPDATE t_cart SET f_quantity = f_quantity + 1 WHERE f_id = %s"
            Database.execute_update(sql, (existing['id'],))
        else:
            sql = "INSERT INTO t_cart (f_user_id, f_product_id,f_quantity,f_status) VALUES (%s, %s,1,1)"
            Database.execute_update(sql, (user_id, product_id))

    @classmethod
    def get_user_cart(cls, user_id):
        sql = """
            SELECT c.f_id cid, p.f_id pid,p.f_name name, p.f_price price, c.f_quantity  quantity
            FROM t_cart c
            JOIN t_product p ON c.f_product_id = p.f_id
            WHERE c.f_user_id = %s and c.f_status=1
        """
        return Database.execute_query(sql, (user_id,))
    @classmethod
    def clear_cart(cls, user_id):
        sql = "UPDATE t_cart SET f_status=2 WHERE f_user_id = %s"
        Database.execute_update(sql, (user_id,))
    @classmethod
    def remove_item(cls, item_id, user_id):
        sql = "UPDATE t_cart SET f_status=0 WHERE f_id = %s AND f_user_id = %s"
        return Database.execute_update(sql, (item_id, user_id))

    @classmethod
    def update_quantity(cls, item_id, user_id, quantity):
        sql = "UPDATE t_cart SET f_quantity = %s WHERE f_id = %s AND f_user_id = %s"
        return Database.execute_update(sql, (quantity, item_id, user_id))

    @classmethod
    def get_item(cls, user_id, product_id):
        sql = "SELECT f_id id,f_user_id user_id,f_product_id product_id ,f_quantity quantity FROM t_cart WHERE f_user_id = %s AND f_product_id = %s AND f_status=1"
        return Database.execute_query(sql, (user_id, product_id), fetch_one=True)
