from functools import wraps
from flask import request, jsonify, g
import jwt
from config import get_config
from app.utils.enums import UserRole

config = get_config()

SECRET_KEY = config.JWT_SECRET_KEY
JWT_ALGORITHM = config.JWT_ALGORITHM

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"success": False, "msg": "Token missing"}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            g.user = payload  # payload should include user basic information(include 'role')
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "msg": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "msg": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, UserRole.USER.value) or g.user.get("role") != UserRole.ADMIN.value:
            return jsonify({"success": False, "msg": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function
