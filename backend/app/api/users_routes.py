from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta, timezone
from app.services.users_service import UsersService
from app.utils.validator import Validator
from app.exceptions import UserNotFoundError
from app.utils.auth_decorators import login_required, admin_required
import os

users_bp = Blueprint('users', __name__)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

@users_bp.route('/', methods=['GET'])
@login_required
@admin_required
def get_all_users():
    try:
        users = UsersService.get_all_users()
        return jsonify({"success": True, "msg": "Login successfully", "data": users}), 200
    except UserNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    validator = Validator()
    validator.required([email, password])
    errors = validator.get_errors()
    if len(errors) > 0:
        return jsonify({"success": False, "msg": str(errors[0])}), 400

    try:
        user = UsersService.login(email, password)
        user["exp"] = datetime.now(timezone.utc) + timedelta(seconds=20) # 新增 exp 欄位（10秒後過期）

        # 登入成功後產生 JWT Token
        token = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)

        return jsonify({"success": True, "msg": "Login successfully", "token": token}), 200
    except UserNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500


@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.json
    user_name = data.get('user_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    # 檢查格式是否符合設定
    validator = Validator()
    validator.required([user_name, email, password, role])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()
    if len(errors) > 0:
        return jsonify({"success": False, "msg": str(errors[0])}), 400

    try:
        user = UsersService.create_user(user_name, email, password, role)
        return jsonify({"success": True, "msg": "Create successfully", "data": user}), 201
    except ValueError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user_by_id(user_id):
    try:
        user = UsersService.get_user_by_id(user_id)
        return jsonify({"success": True, "msg": "Get successfully", "data": user}), 200
    except UserNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        user = UsersService.delete_user(user_id)
        return jsonify({"success": True, "msg": "Delete successfully", "data": user}), 200
    except UserNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500
    