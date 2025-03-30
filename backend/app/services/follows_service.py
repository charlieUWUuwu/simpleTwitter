
from app.repositories.follows_repository import FollowsRepository

class FollowsService:
    @staticmethod
    def get_follow(follow_id: int, followed_id: int):
        return FollowsRepository.get_follow(follow_id, followed_id)

    @staticmethod
    def create_follow(follow_id: int, followed_id: int):
        return FollowsRepository.create_follow(follow_id, followed_id)
    
    @staticmethod
    def delete_follow(follow_id: int, followed_id: int):
        follow = FollowsRepository.get_follow(follow_id, followed_id)
        if follow:
            FollowsRepository.delete_follow(follow_id, followed_id)
            return follow
        return None