import os
import pymysql
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

class Config:
    APP_HOST = "localhost"
    APP_PORT = 5001
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3307
    MYSQL_DB = "db_twitter"
    MYSQL_CHARSET = "utf8mb4"
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_CURSORCLASS=pymysql.cursors.DictCursor  # 查詢結果以字典形式回傳

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


def get_config():
    if os.getenv("ENV_MODE") == "production":
        return ProductionConfig
    elif os.getenv("ENV_MODE") == "development":
        return DevelopmentConfig
    else:
        # default
        return DevelopmentConfig