from app.database.db import Database

class FollowsRepository:
    @staticmethod
    def get_follow(user_id1: int, user_id2: int):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Follows WHERE user_id1 = %s AND user_id2 = %s"
                cursor.execute(sql, (user_id1, user_id2))
                follow = cursor.fetchone()
                return follow
        finally:
            connection.close()

    @staticmethod
    def create_follow(user_id1: int, user_id2: int):
        connection = Database.get_db_connection()        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO Follows (user_id1, user_id2) VALUES (%s, %s)"
                cursor.execute(sql, (user_id1, user_id2))
                connection.commit()
                
                return {"user_id1": user_id1, "user_id2": user_id2}
        finally:
            connection.close()

    @staticmethod
    def delete_follow(user_id1: int, user_id2: int):
        connection = Database.get_db_connection()        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM Follows WHERE user_id1 = %s AND user_id2 = %s"
                cursor.execute(sql, (user_id1, user_id2))
                connection.commit()
        finally:
            connection.close()
