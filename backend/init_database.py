from config import config
import pymysql

DB_CONFIG = {
    "host": config["development"].MYSQL_HOST,
    "user": config["development"].MYSQL_USER,
    "password": config["development"].MYSQL_PASSWORD,
    "database": config["development"].MYSQL_DB,
    "port": config["development"].MYSQL_PORT,
    "charset": config["development"].CHARSET,
    "cursorclass": pymysql.cursors.DictCursor
}

user_input = input("你確定真的要重新初始化資料庫嗎？確定的話請打：「I'm really super clear what I'm doing」\n")
if user_input != "I'm really super clear what I'm doing":
    print("拒絕初始化資料庫")
    exit(0)

connection = pymysql.connect(**DB_CONFIG)

cursor = connection.cursor()

# 表的刪除順序需要考量到 Foreign key
cursor.execute("DROP TABLE IF EXISTS Follows")
cursor.execute("DROP TABLE IF EXISTS Tweets")
cursor.execute("DROP TABLE IF EXISTS Users")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Users(
        user_id INT AUTO_INCREMENT NOT NULL,
        name VARCHAR(70) NOT NULL,
        email VARCHAR(70) NOT NULL UNIQUE,
        salt VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (user_id)
    )
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Tweets(
        tweet_id INT AUTO_INCREMENT NOT NULL,
        user_id INT NOT NULL,
        creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        content TEXT NOT NULL,
        PRIMARY KEY (tweet_id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    )
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Follows(
        follow_id INT NOT NULL,
        followed_id INT NOT NULL,
        PRIMARY KEY (follow_id, followed_id),
        FOREIGN KEY (follow_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (followed_id) REFERENCES Users(user_id) ON DELETE CASCADE
    )
    """
)
connection.commit()
print("Tables initialized successfully!")