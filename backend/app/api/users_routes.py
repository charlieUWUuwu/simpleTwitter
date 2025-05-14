import os
from datetime import datetime, timedelta, timezone

import jwt
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.services.users_service import UsersService
from app.utils.auth_decorators import admin_required, login_required
from app.utils.validator import Validator

users_bp = Blueprint("users", __name__)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


@users_bp.route("/", methods=["GET"])
@login_required
@admin_required
@swag_from(
    {
        "tags": ["Users"],
        "summary": "取得所有使用者（需登入+管理員）",
        "responses": {
            200: {
                "description": "成功取得使用者清單",
                "examples": {
                    "application/json": {
                        "msg": "Login successfully",
                        "success": True,
                        "data": [
                            {
                                "email": "123@gmail.com",
                                "name": "AA",
                                "role": "user",
                                "user_id": 1,
                            },
                            {
                                "email": "456@gmail.com",
                                "name": "BB",
                                "role": "admin",
                                "user_id": 2,
                            },
                            {
                                "email": "new@example.com",
                                "name": "newuser",
                                "role": "user",
                                "user_id": 3,
                            },
                        ],
                    }
                },
            }
        },
    }
)
def get_all_users():
    users = UsersService.get_all_users()
    return jsonify({"success": True, "msg": "Login successfully", "data": users}), 200


@users_bp.route("/login", methods=["POST"])
@swag_from(
    {
        "tags": ["Users"],
        "summary": "使用者登入",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "example": "new@example.com"},
                        "password": {"type": "string", "example": "password123@"},
                    },
                    "required": ["email", "password"],
                },
            }
        ],
        "responses": {
            200: {
                "description": "登入成功，回傳 JWT Token",
                "examples": {
                    "application/json": {
                        "success": True,
                        "msg": "Login successfully",
                        "token": "jwt_token_here",
                    }
                },
            },
            400: {"description": "欄位錯誤"},
        },
    }
)
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    validator = Validator()
    validator.required([email, password])
    errors = validator.get_errors()
    if len(errors) > 0:
        return jsonify({"success": False, "msg": str(errors[0])}), 400

    user = UsersService.login(email, password)
    user["exp"] = datetime.now(timezone.utc) + timedelta(
        hours=2
    )  # 新增 exp 欄位（2小時後過期）

    # 登入成功後產生 JWT Token
    token = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)

    return jsonify({"success": True, "msg": "Login successfully", "token": token}), 200


@users_bp.route("/register", methods=["POST"])
@swag_from(
    {
        "tags": ["Users"],
        "summary": "註冊新使用者",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_name": {"type": "string", "example": "newuser"},
                        "email": {"type": "string", "example": "new@example.com"},
                        "password": {"type": "string", "example": "password123@"},
                        "role": {"type": "string", "example": "user"},
                    },
                    "required": ["user_name", "email", "password"],
                },
            }
        ],
        "responses": {
            201: {
                "description": "註冊成功",
                "examples": {
                    "application/json": {
                        "data": {
                            "email": "new@example.com",
                            "name": "newuser",
                            "role": "user",
                            "user_id": 3,
                        },
                        "msg": "Create successfully",
                        "success": True,
                    }
                },
            },
            400: {"description": "格式錯誤"},
        },
    }
)
def create_user():
    data = request.json
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    # 檢查格式是否符合設定
    validator = Validator()
    validator.required([user_name, email, password, role])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()
    if len(errors) > 0:
        return jsonify({"success": False, "msg": str(errors[0])}), 400

    user = UsersService.create_user(user_name, email, password, role)
    return jsonify({"success": True, "msg": "Create successfully", "data": user}), 201


@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
@swag_from(
    {
        "tags": ["Users"],
        "summary": "透過 ID 取得使用者資料（需登入）",
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
                "description": "取得成功",
                "examples": {
                    "application/json": {
                        "msg": "Get successfully",
                        "success": True,
                        "data": {
                            "email": "new@example.com",
                            "name": "newuser",
                            "role": "user",
                            "user_id": 3,
                        },
                    }
                },
            }
        },
    }
)
def get_user_by_id(user_id):
    user = UsersService.get_user_by_id(user_id)
    return jsonify({"success": True, "msg": "Get successfully", "data": user}), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
@admin_required
@swag_from(
    {
        "tags": ["Users"],
        "summary": "刪除使用者（需登入 + 管理員）",
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
                "description": "刪除成功",
                "examples": {
                    "application/json": {
                        "msg": "Delete successfully",
                        "success": True,
                        "data": {
                            "email": "new@example.com",
                            "name": "newuser",
                            "role": "user",
                            "user_id": 3,
                        },
                    }
                },
            }
        },
    }
)
def delete_user(user_id):
    user = UsersService.delete_user(user_id)
    return jsonify({"success": True, "msg": "Delete successfully", "data": user}), 200
