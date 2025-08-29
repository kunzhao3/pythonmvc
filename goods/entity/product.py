from goods.libs.database import Database


class Product:
    """商品模型"""
    @classmethod
    def get_all(cls):
        return Database.execute_query("SELECT f_id id,f_name name,f_price price FROM t_product")

    @classmethod
    def get_by_id(cls, product_id):
        sql = "SELECT f_id id,f_name name,f_price price FROM t_product WHERE f_id = %s"
        return Database.execute_query(sql, (product_id,), fetch_one=True)
