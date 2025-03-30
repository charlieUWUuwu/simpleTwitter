import secrets
from hashlib import sha256
from app.repositories.users_repository import UsersRepository

# 若執行失敗或是抓取不到用戶資料，回傳 None

class UsersService:
    @staticmethod
    def login(email: str, password: str):
        # 檢查 email 是否已經被註冊過
        user = UsersRepository.get_user_by_email(email)
        if user == None:
            return None
        
        hashed_password = sha256((password + user['salt']).encode('utf-8')).hexdigest()

        if hashed_password == user['password']:
            user.pop('password')
            user.pop('salt')
            return user
        return None

    @staticmethod
    def create_user(user_name: str, email: str, password: str):
        # 檢查 email 是否已經被註冊過
        user = UsersRepository.get_user_by_email(email)
        if not user:
            salt = secrets.token_hex(16)  # 生成 16 位的隨機 salt
            hashed_password = sha256((password + salt).encode('utf-8')).hexdigest()
            user = UsersRepository.create_user(user_name, email, salt, hashed_password)
            user.pop('password')
            user.pop('salt')
            return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id: int):
        user = UsersRepository.get_user_by_id(user_id)
        if user:
            user.pop('password')
            user.pop('salt')
            return user
        return None
    
    @staticmethod
    def get_all_users():
        user_list = UsersRepository.get_all_users()
        if user_list:
            for user in user_list:
                user.pop('password')
                user.pop('salt')
            return user_list
        return None
    
    @staticmethod
    def delete_user(user_id: int):
        user = UsersRepository.get_user_by_id(user_id)
        if user:
            UsersRepository.delete_user(user_id)
            # 回傳被刪除的 user 資訊
            user.pop('password')
            user.pop('salt')
            return user
        return None