from app.database.db import Database


class TweetsRepository:
    @staticmethod
    def create_tweet(user_id: int, content: str, creation_time: str):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO Tweets (user_id, creation_time, content) VALUES (%s, %s, %s)"
                cursor.execute(sql, (user_id, creation_time, content))
                connection.commit()

                # 獲取最近一次 insert 操作後自動生成的 id
                tweet_id = cursor.lastrowid
                return {
                    "tweet_id": tweet_id,
                    "user_id": user_id,
                    "content": content,
                    "creation_time": creation_time,
                }
        finally:
            connection.close()

    @staticmethod
    def get_tweets_by_userid(user_id: int):
        # 獲取特定用戶的所有推文
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Tweets WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                tweets = cursor.fetchall()
                return tweets
        finally:
            connection.close()

    @staticmethod
    def get_tweet_by_id(tweet_id: int):
        # 獲取特定用戶的所有推文
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Tweets WHERE tweet_id = %s"
                cursor.execute(sql, (tweet_id,))
                tweet = cursor.fetchone()
                return tweet
        finally:
            connection.close()

    @staticmethod
    def get_all_tweets():
        # 獲取所有用戶的所有推文
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Tweets"
                cursor.execute(sql)
                tweets = cursor.fetchall()
                return tweets
        finally:
            connection.close()

    @staticmethod
    def delete_tweet(tweet_id: int):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM Tweets WHERE tweet_id = %s"
                cursor.execute(sql, (tweet_id,))
                connection.commit()
        finally:
            connection.close()
