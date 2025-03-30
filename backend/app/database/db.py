# 處理資料庫的連線

import pymysql
from config import config

db_config = config["development"]

DB_CONFIG = {
    "host": db_config.MYSQL_HOST,
    "user": db_config.MYSQL_USER,
    "password": db_config.MYSQL_PASSWORD,
    "database": db_config.MYSQL_DB,
    "port": db_config.MYSQL_PORT,
    "cursorclass": pymysql.cursors.DictCursor
}

class Database:
    @staticmethod
    def get_db_connection():
        return pymysql.connect(**DB_CONFIG)