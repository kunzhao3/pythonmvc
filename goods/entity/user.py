from werkzeug.security import generate_password_hash, check_password_hash
from goods.libs.database import Database


class User:
    """用户模型"""
    def __init__(cls, user_data):
        cls.id = user_data.get('f_id')
        cls.username = user_data.get('f_username')
        cls.password_hash = user_data.get('f_password_hash')
    @classmethod
    def create(cls, username, password):
        hashed_pw = generate_password_hash(password)
        sql = "INSERT INTO t_user (f_username, f_password_hash) VALUES (%s, %s)"
        return Database.execute_update(sql, (username, hashed_pw))

    @classmethod
    def get_by_username(cls, username):
        sql = "SELECT f_id ,f_username, f_password_hash  FROM t_user WHERE f_username = %s"
        user_data = Database.execute_query(sql, (username,), fetch_one=True)
        return cls(user_data) if user_data else None

    @classmethod
    def verify_password(cls, stored_hash, password):
        return check_password_hash(stored_hash, password)
