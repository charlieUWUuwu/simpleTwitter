from datetime import datetime
from app.repositories.tweets_repository import TweetsRepository
from app.repositories.users_repository import UsersRepository
from app.exceptions import UserNotFoundError, TweetNotFoundError

class TweetsService:
    @staticmethod
    def create_tweet(user_id: int, content: str):
        creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return TweetsRepository.create_tweet(user_id, content, creation_time)
    
    @staticmethod
    def get_tweet_by_userid(user_id: int):
        return TweetsRepository.get_tweet_by_userid(user_id)
    
    @staticmethod
    def get_all_tweets():
        return TweetsRepository.get_all_tweets()