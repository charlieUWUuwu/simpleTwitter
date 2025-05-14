from flask import Blueprint, jsonify, request

from app.services.tweets_service import TweetsService

tweets_bp = Blueprint("tweets", __name__)


@tweets_bp.route("/", methods=["GET"])
def get_all_tweets():
    tweets = TweetsService.get_all_tweets()
    return jsonify({"success": True, "msg": "Login successfully", "data": tweets}), 200


@tweets_bp.route("/user/<int:user_id>", methods=["GET"])
def get_tweets_by_userid(user_id):
    tweets = TweetsService.get_tweets_by_userid(user_id)
    return jsonify({"success": True, "msg": "Get successfully", "data": tweets}), 200


@tweets_bp.route("/<int:tweet_id>", methods=["GET"])
def get_tweet_by_id(tweet_id):
    tweet = TweetsService.get_tweet_by_id(tweet_id)
    return jsonify({"success": True, "msg": "Get successfully", "data": tweet}), 200


@tweets_bp.route("/tweet", methods=["POST"])
def create_tweet():
    data = request.json
    user_id = data.get("user_id")
    content = data.get("content")

    if user_id is None or content is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    tweet = TweetsService.create_tweet(user_id, content)
    return (
        jsonify({"success": True, "msg": "Create tweet successfully", "data": tweet}),
        201,
    )


@tweets_bp.route("/<int:tweet_id>", methods=["DELETE"])
def delet_tweet(tweet_id):
    if tweet_id is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    tweet = TweetsService.delete_tweet(tweet_id)
    return (
        jsonify({"success": True, "msg": "Delete follow successfully", "data": tweet}),
        200,
    )
