from app.repositories.follows_repository import FollowsRepository
from app.repositories.users_repository import UsersRepository
from app.exceptions import UserNotFoundError, FollowNotFoundError

class FollowsService:
    @staticmethod
    def get_all_follows():
        follow_list = FollowsRepository.get_all_follows()
        if not follow_list:
            raise FollowNotFoundError("No follows")
        return follow_list

    @staticmethod
    def create_follow(user_id1: int, user_id2: int):
        if UsersRepository.get_user_by_id(user_id1) is None or UsersRepository.get_user_by_id(user_id2) is None:
            raise UserNotFoundError("User ID not found")
        if FollowsRepository.get_follow(user_id1, user_id2):
            raise ValueError("Follow already exists")
        follow = FollowsRepository.create_follow(user_id1, user_id2)
        return follow
    
    @staticmethod
    def delete_follow(user_id1: int, user_id2: int):
        if UsersRepository.get_user_by_id(user_id1) is None or UsersRepository.get_user_by_id(user_id2) is None:
            raise UserNotFoundError("User ID not found")
        
        follow = FollowsRepository.get_follow(user_id1, user_id2)
        if not follow:
            raise FollowNotFoundError("Follow not found")
        
        # 回傳刪除的 follow
        FollowsRepository.delete_follow(user_id1, user_id2)
        return follow
 
