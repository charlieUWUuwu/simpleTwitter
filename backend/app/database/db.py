# 處理資料庫的連線

import pymysql
from dbutils.pooled_db import PooledDB

from config import get_config

config = get_config()

# 初始化連線池（只需初始化一次，供全域使用）
POOL = PooledDB(
    creator=pymysql,  # 指定使用 pymysql 模組來建立連線
    maxconnections=10,  # 連線池允許的最大連線數
    mincached=2,  # 初始化時，最少建立的空閒連線數
    maxcached=5,  # 連線池中允許的最大空閒連線數
    blocking=True,  # 若連線數已達上限，是否等待可用連線（True 代表等待）
    maxusage=None,  # 單一連線的最大重複使用次數，None 表示不限制
    ping=0,  # 檢查資料庫連線是否可用，0 表示從不檢查
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DB,
    port=config.MYSQL_PORT,
    charset=config.MYSQL_CHARSET,
    cursorclass=config.MYSQL_CURSORCLASS,
)


class Database:
    @staticmethod
    def get_db_connection():
        return POOL.connection()
