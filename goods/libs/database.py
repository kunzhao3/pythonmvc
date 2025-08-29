import threading
from contextlib import contextmanager
from queue import Queue

import pymysql.cursors
from goods.config.config import  Configure


@Configure
def get_db_config(cfg):
    return cfg['database']

class Database:
    """数据库操作基类"""
    db_config = get_db_config()
    _conn_params = {
        'host': db_config.get('host'),
        'port': db_config.get('port'),
        'user': db_config.get('user'),
        'password': db_config.get('password'),
        'db': db_config.get('db'),
        'charset': 'utf8mb4',
        'autocommit':True,
        "cursorclass": pymysql.cursors.DictCursor  # 关键配置，非常重要
    }
    # 内置默认配置（直接修改类属性即可覆盖）
    _max_connections = db_config.get('max_connections')  # 最大连接数
    # 线程安全连接池
    _pool = None
    _lock = threading.Lock()

    @classmethod
    def _initialize_pool(cls):
        """首次使用时自动初始化连接池"""
        if cls._pool is None:
            with cls._lock:
                if cls._pool is None:
                    cls._pool = Queue(maxsize=cls._max_connections)
                    # 预填充连接
                    for _ in range(cls._max_connections):
                        conn = cls._create_connection()
                        cls._pool.put(conn)

    @classmethod
    def _create_connection(cls):
        """根据类属性创建新连接"""
        return pymysql.connect(**cls._conn_params)

    @classmethod
    @contextmanager
    def get_connection(cls):
        """安全获取连接（自动检测有效性）"""
        cls._initialize_pool()
        conn = None
        try:
            with cls._lock:
                if not cls._pool.empty():
                    conn = cls._pool.get()
                else:
                    conn = cls._create_connection()  # 动态扩容
            # 检查连接是否存活
            conn.ping(reconnect=True)
            yield conn
        finally:
            if conn:
                with cls._lock:
                    if cls._pool.qsize() < cls._max_connections:
                        cls._pool.put(conn)
                    else:
                        conn.close()  # 关闭多余连接

    @classmethod
    def execute_query(cls, sql, params=(), fetch_one=False):
        with cls.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone() if fetch_one else cursor.fetchall()


    @classmethod
    def execute_update(cls, sql, params=()):
        with cls.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                return cursor.lastrowid