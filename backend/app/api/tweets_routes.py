from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services.tweets_service import TweetsService

tweets_bp = Blueprint("tweets", __name__)


@tweets_bp.route("/", methods=["GET"])
@swag_from(
    {
        "tags": ["Tweets"],
        "summary": "取得所有推文",
        "responses": {
            200: {
                "description": "成功取得所有推文",
                "examples": {
                    "application/json": {
                        "msg": "Login successfully",
                        "success": True,
                        "data": [
                            {
                                "content": "今天天氣真棒！",
                                "creation_time": "Wed, 14 May 2025 18:14:34 GMT",
                                "tweet_id": 1,
                                "user_id": 1,
                            }
                        ],
                    }
                },
            }
        },
    }
)
def get_all_tweets():
    tweets = TweetsService.get_all_tweets()
    return jsonify({"success": True, "msg": "Login successfully", "data": tweets}), 200


@tweets_bp.route("/user/<int:user_id>", methods=["GET"])
@swag_from(
    {
        "tags": ["Tweets"],
        "summary": "透過使用者 ID 取得推文",
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "使用者 ID",
            }
        ],
        "responses": {
            200: {
                "description": "成功取得指定使用者的推文",
                "examples": {
                    "application/json": {
                        "msg": "Get successfully",
                        "success": True,
                        "data": [
                            {
                                "content": "今天天氣真棒！",
                                "creation_time": "Wed, 14 May 2025 18:14:34 GMT",
                                "tweet_id": 1,
                                "user_id": 1,
                            }
                        ],
                    }
                },
            }
        },
    }
)
def get_tweets_by_userid(user_id):
    tweets = TweetsService.get_tweets_by_userid(user_id)
    return jsonify({"success": True, "msg": "Get successfully", "data": tweets}), 200


@tweets_bp.route("/<int:tweet_id>", methods=["GET"])
@swag_from(
    {
        "tags": ["Tweets"],
        "summary": "透過推文 ID 取得推文",
        "parameters": [
            {
                "name": "tweet_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "推文 ID",
            }
        ],
        "responses": {
            200: {
                "description": "成功取得指定使用者的推文",
                "examples": {
                    "application/json": {
                        "msg": "Get successfully",
                        "success": True,
                        "data": {
                            "content": "今天天氣真棒！",
                            "creation_time": "Wed, 14 May 2025 18:14:34 GMT",
                            "tweet_id": 1,
                            "user_id": 1,
                        },
                    }
                },
            }
        },
    }
)
def get_tweet_by_id(tweet_id):
    tweet = TweetsService.get_tweet_by_id(tweet_id)
    return jsonify({"success": True, "msg": "Get successfully", "data": tweet}), 200


@tweets_bp.route("/tweet", methods=["POST"])
@swag_from(
    {
        "tags": ["Tweets"],
        "summary": "建立新推文",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "int", "example": 1},
                        "content": {"type": "string", "example": "今天天氣真棒！"},
                    },
                    "required": ["user_id", "content"],
                },
            }
        ],
        "responses": {
            201: {
                "description": "成功建立推文",
                "examples": {
                    "application/json": {
                        "msg": "Create tweet successfully",
                        "success": True,
                        "data": {
                            "content": "今天天氣真棒！",
                            "creation_time": "2025-05-14 18:14:34",
                            "tweet_id": 1,
                            "user_id": 1,
                        },
                    }
                },
            },
            400: {"description": "欄位缺漏"},
        },
    }
)
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
@swag_from(
    {
        "tags": ["Tweets"],
        "summary": "刪除推文",
        "parameters": [
            {
                "name": "tweet_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "推文 ID",
            }
        ],
        "responses": {
            200: {
                "description": "刪除成功",
                "examples": {
                    "application/json": {
                        "msg": "Delete follow successfully",
                        "success": True,
                        "data": {
                            "content": "今天天氣真棒！",
                            "creation_time": "Wed, 14 May 2025 18:14:34 GMT",
                            "tweet_id": 1,
                            "user_id": 1,
                        },
                    }
                },
            },
            400: {"description": "缺少必要參數"},
        },
    }
)
def delet_tweet(tweet_id):
    if tweet_id is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    tweet = TweetsService.delete_tweet(tweet_id)
    return (
        jsonify({"success": True, "msg": "Delete follow successfully", "data": tweet}),
        200,
    )
