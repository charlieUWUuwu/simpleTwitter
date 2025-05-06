from flask import Blueprint, request, jsonify
from app.services.follows_service import FollowsService

follows_bp = Blueprint('follows', __name__)

@follows_bp.route('/', methods=['GET'])
def get_all_follows():
    follows = FollowsService.get_all_follows()
    return jsonify({"success": True, "msg": "Get all follows successfully", "data": follows}), 200


@follows_bp.route('/follow', methods=['POST'])
def follow_user():
    data = request.json
    user_id1 = data.get('user_id1')
    user_id2 = data.get('user_id2')
    if user_id1 is None or user_id2 is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    follow = FollowsService.create_follow(user_id1, user_id2)
    return jsonify({"success": True, "msg": "Create follow successfully", "data": follow}), 201


@follows_bp.route('/<int:user_id1>/<int:user_id2>', methods=['DELETE'])
def unfollow_user(user_id1, user_id2):
    if user_id1 is None or user_id2 is None:
        return jsonify({"success": False, "msg": "Missing required fields"}), 400

    follow = FollowsService.delete_follow(user_id1, user_id2)
    return jsonify({"success": True, "msg": "Delete follow successfully", "data": follow}), 200
