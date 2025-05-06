from datetime import datetime
from app.repositories.tweets_repository import TweetsRepository
from app.repositories.users_repository import UsersRepository
from app.utils.exceptions import UserNotFoundError, TweetNotFoundError

class TweetsService:
    @staticmethod
    def create_tweet(user_id: int, content: str):
        creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if UsersRepository.get_user_by_id(user_id) is None:
            raise UserNotFoundError("User ID not found")
        
        tweet = TweetsRepository.create_tweet(user_id, content, creation_time)
        return tweet
    
    @staticmethod
    def get_tweets_by_userid(user_id: int):
        if not UsersRepository.get_user_by_id(user_id):
            raise UserNotFoundError("User not found")
        
        tweet_list = TweetsRepository.get_tweets_by_userid(user_id)
        if not tweet_list:
            raise TweetNotFoundError("Tweet not found")
        return tweet_list
    
    @staticmethod
    def get_tweet_by_id(tweet_id: int):
        tweet = TweetsRepository.get_tweet_by_id(tweet_id)
        if not tweet:
            raise TweetNotFoundError("Tweet not found")
        return tweet
    
    @staticmethod
    def get_all_tweets():
        tweet_list = TweetsRepository.get_all_tweets()
        if not tweet_list:
            raise TweetNotFoundError("No tweets")
        return tweet_list
    
    @staticmethod
    def delete_tweet(tweet_id: int):
        tweet = TweetsRepository.get_tweet_by_id(tweet_id)
        if not tweet:
            raise TweetNotFoundError("Tweet not found")

        # 回傳刪除的 tweet
        TweetsRepository.delete_tweet(tweet_id)
        return tweet