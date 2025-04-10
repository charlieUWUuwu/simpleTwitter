# 處理資料庫的連線

import pymysql
from dbutils.pooled_db import PooledDB
from config import config

db_config = config["development"]

# 初始化連線池（只需初始化一次，供全域使用）
POOL = PooledDB(
    creator=pymysql,              # 指定使用 pymysql 模組來建立連線
    maxconnections=10,            # 連線池允許的最大連線數
    mincached=2,                  # 初始化時，最少建立的空閒連線數
    maxcached=5,                  # 連線池中允許的最大空閒連線數
    blocking=True,                # 若連線數已達上限，是否等待可用連線（True 代表等待）
    maxusage=None,                # 單一連線的最大重複使用次數，None 表示不限制
    ping=0,                       # 檢查資料庫連線是否可用，0 表示從不檢查
    host=db_config.MYSQL_HOST,
    user=db_config.MYSQL_USER,
    password=db_config.MYSQL_PASSWORD,
    database=db_config.MYSQL_DB,
    port=db_config.MYSQL_PORT,
    charset=db_config.CHARSET,
    cursorclass=pymysql.cursors.DictCursor  # 查詢結果以字典形式回傳
)

class Database:
    @staticmethod
    def get_db_connection():
        return POOL.connection()
