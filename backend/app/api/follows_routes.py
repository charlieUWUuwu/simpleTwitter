from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services.follows_service import FollowsService

follows_bp = Blueprint("follows", __name__)


@follows_bp.route("/", methods=["GET"])
@swag_from(
    {
        "tags": ["Follows"],
        "summary": "取得所有追蹤關係",
        "responses": {
            200: {
                "description": "成功取得所有追蹤資料",
                "examples": {
                    "application/json": {
                        "msg": "Get all follows successfully",
                        "success": True,
                        "data": [{"user_id1": 1, "user_id2": 2}],
                    }
                },
            }
        },
    }
)
def get_all_follows():
    follows = FollowsService.get_all_follows()
    return (
        jsonify(
            {"success": True, "msg": "Get all follows successfully", "data": follows}
        ),
        200,
    )


@follows_bp.route("/follow", methods=["POST"])
@swag_from(
    {
        "tags": ["Follows"],
        "summary": "建立追蹤關係",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id1": {"type": "int", "example": 1},
                        "user_id2": {"type": "int", "example": 2},
                    },
                    "required": ["user_id1", "user_id2"],
                },
            }
        ],
        "responses": {
            201: {
                "description": "追蹤建立成功",
                "examples": {
                    "application/json": {
                        "msg": "Create follow successfully",
                        "success": True,
                        "data": {"user_id1": 1, "user_id2": 2},
                    }
                },
            },
            400: {"description": "缺少必要欄位"},
        },
    }
)
def follow_user():
    data = request.json
    user_id1 = data.get("user_id1")
    user_id2 = data.get("user_id2")
    if user_id1 is None or user_id2 is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    follow = FollowsService.create_follow(user_id1, user_id2)
    return (
        jsonify({"success": True, "msg": "Create follow successfully", "data": follow}),
        201,
    )


@follows_bp.route("/<int:user_id1>/<int:user_id2>", methods=["DELETE"])
@swag_from(
    {
        "tags": ["Follows"],
        "summary": "取消追蹤關係",
        "parameters": [
            {
                "name": "user_id1",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "追蹤者的 user_id",
            },
            {
                "name": "user_id2",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "被追蹤者的 user_id",
            },
        ],
        "responses": {
            200: {
                "description": "取消追蹤成功",
                "examples": {
                    "application/json": {
                        "msg": "Delete follow successfully",
                        "success": True,
                        "data": {"user_id1": 1, "user_id2": 2},
                    }
                },
            },
            400: {"description": "缺少必要欄位"},
        },
    }
)
def unfollow_user(user_id1, user_id2):
    if user_id1 is None or user_id2 is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    follow = FollowsService.delete_follow(user_id1, user_id2)
    return (
        jsonify({"success": True, "msg": "Delete follow successfully", "data": follow}),
        200,
    )
