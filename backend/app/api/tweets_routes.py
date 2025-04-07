from flask import Blueprint, request, jsonify
from app.services.tweets_service import TweetsService
from app.utils.validator import Validator

tweets_bp = Blueprint('tweets', __name__)

@tweets_bp.route('/', methods=['GET'])
def get_all_tweets():
    tweets = TweetsService.get_all_tweets()
    if tweets is None:
        return jsonify({"msg": "No posts exist"}), 200
    return jsonify(tweets), 200

@tweets_bp.route('/<int:user_id>', methods=['GET'])
def get_tweet_by_userid(user_id):
    tweets = TweetsService.get_tweet_by_userid(user_id)
    if tweets is None:
        return jsonify({"msg": "No posts exist"}), 200
    return jsonify(tweets), 200

@tweets_bp.route('/create', methods=['POST'])
def create_tweet():
    data = request.json
    user_id = data.get('user_id')
    content = data.get('content')

    if user_id is None or content is None:
        return jsonify({"msg": "Missing required fields"}), 400
    if TweetsService.create_tweet(user_id, content) is None:
        return jsonify({"msg": "Tweet creation failed"}), 400
    return jsonify({"msg": "Tweet created successfully"}), 201