from flask import Blueprint, request, jsonify
from app.services.follows_service import FollowsService
from app.exceptions import UserNotFoundError, FollowNotFoundError

follows_bp = Blueprint('follows', __name__)

@follows_bp.route('/', methods=['GET'])
def get_all_follows():
    try:
        follows = FollowsService.get_all_follows()
        return jsonify({"success": True, "msg": "Get all follows successfully", "data": follows}), 200
    except UserNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except FollowNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500


@follows_bp.route('/follow', methods=['POST'])
def follow_user():
    data = request.json
    user_id1 = data.get('user_id1')
    user_id2 = data.get('user_id2')
    if user_id1 is None or user_id2 is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    try:
        follow = FollowsService.create_follow(user_id1, user_id2)
        return jsonify({"success": True, "msg": "Create follow successfully", "data": follow}), 201
    except UserNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500

@follows_bp.route('/<int:user_id1>/<int:user_id2>', methods=['DELETE'])
def unfollow_user(user_id1, user_id2):
    if user_id1 is None or user_id2 is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    try:
        follow = FollowsService.delete_follow(user_id1, user_id2)
        return jsonify({"success": True, "msg": "Delete follow successfully", "data": follow}), 200
    except UserNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except FollowNotFoundError as e:
        return jsonify({"success": False, "msg": str(e)}), 404
    except ValueError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "msg": "Internal server error"}), 500
