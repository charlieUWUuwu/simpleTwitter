from app.database.db import Database

class UsersRepository:
    @staticmethod
    def create_user(name: str, email: str, salt: str, password: str):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO Users (name, email, salt, password) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, email, salt, password))
                connection.commit()
                
                user_id = cursor.lastrowid
                return {
                    "user_id": user_id, 
                    "name": name, 
                    "email": email, 
                    "salt": salt, 
                    "password": password
                }
        finally:
            connection.close()

    @staticmethod
    def get_user_by_id(user_id: int):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Users WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                user = cursor.fetchone()
                return user or None
        finally:
            connection.close()

    @staticmethod
    def get_user_by_email(email: str):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Users WHERE email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                return user or None
        finally:
            connection.close()

    @staticmethod
    def get_all_users():
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Users"
                cursor.execute(sql)
                users = cursor.fetchall()
                if len(users) > 0:
                    return users
                return None
        finally:
            connection.close()

    @staticmethod
    def delete_user(user_id: int):
        connection = Database.get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM Users WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                connection.commit()
        finally:
            connection.close()