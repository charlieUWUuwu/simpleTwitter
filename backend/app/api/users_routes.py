from flask import Blueprint, request, jsonify
from app.services.users_service import UsersService
from app.utils.validator import Validator

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    users = UsersService.get_all_users()
    if users is None:
        return jsonify({"msg": "Ｕser not found"})
    return jsonify(users), 200

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if UsersService.login(email, password) is None:
        return jsonify({"msg": "Login failed"}), 401
    return jsonify({"msg": "Login successfully"}), 200

@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.json
    user_name = data.get('user_name')
    email = data.get('email')
    password = data.get('password')

    # 檢查格式是否符合設定
    validator = Validator()
    validator.required([user_name, email, password])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()

    # 判定是否錯誤，沒有的話回傳成功訊息與狀態碼
    if len(errors) > 0:
        return jsonify({"msg": str(errors[0])}), 400
    
    user = UsersService.create_user(user_name, email, password)
    if user is None:
        return jsonify({"msg": "Email has been registered"}), 400
    return jsonify({"msg": "User created successfully"}), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UsersService.get_user_by_id(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UsersService.delete_user(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user), 200
    