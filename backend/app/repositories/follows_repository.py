from app.database.db import Database

class FollowsRepository:
    @staticmethod
    def get_follow(follow_id: int, followed_id: int):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Follows WHERE follow_id = %s AND followed_id = %s"
                cursor.execute(sql, (follow_id, followed_id))
                return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def create_follow(follow_id: int, followed_id: int):
        connection = Database.get_db_connection()        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO Follows (follow_id, followed_id) VALUES (%s, %s)"
                cursor.execute(sql, (follow_id, followed_id))
                connection.commit()
                
                return {"follow_id": follow_id, "followed_id": followed_id}
        finally:
            connection.close()

    @staticmethod
    def delete_follow(follow_id: int, followed_id: int):
        connection = Database.get_db_connection()        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM Follows WHERE follow_id = %s AND followed_id = %s"
                cursor.execute(sql, (follow_id, followed_id))
                connection.commit()
        finally:
            connection.close()
