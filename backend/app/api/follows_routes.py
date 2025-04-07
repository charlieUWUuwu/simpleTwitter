from flask import Blueprint, request, jsonify
from app.services.follows_service import FollowsService

follows_bp = Blueprint('follows', __name__)

@follows_bp.route('/<int:follow_id>/<int:followed_id>', methods=['GET'])
def get_one_follow(follow_id, followed_id):
    if follow_id is None or followed_id is None:
        return jsonify({"msg": "Missing required fields"}), 400
    if not FollowsService.get_follow(follow_id, followed_id):
        return jsonify({"msg": "Follow not found"}), 404
    return jsonify({"msg": "Successful"}), 200

@follows_bp.route('/follow', methods=['POST'])
def follow_user():
    data = request.json
    follow_id = data.get('follow_id')
    followed_id = data.get('followed_id')

    if follow_id is None or followed_id is None:
        return jsonify({"msg": "Missing required fields"}), 400
    if not FollowsService.follow_user(follow_id, followed_id):
        return jsonify({"msg": "Follow failed"}), 400
    
    return jsonify({"msg": "Followed successfully"}), 201

@follows_bp.route('/unfollow', methods=['DELETE'])
def unfollow_user():
    data = request.json
    follow_id = data.get('follow_id')
    followed_id = data.get('followed_id')
    
    if follow_id is None or followed_id is None:
        return jsonify({"msg": "Missing required fields"}), 400
    if not FollowsService.delete_follow(follow_id, followed_id):
        return jsonify({"msg": "Follow not found"}), 400
    
    return jsonify({"msg": "Followed successfully"}), 201
