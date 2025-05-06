# error_handlers.py
from flask import jsonify
from app.utils.exceptions import UserNotFoundError, FollowNotFoundError, TweetNotFoundError

def register_error_handlers(app):
    @app.errorhandler(UserNotFoundError)
    def handle_user_not_found(error):
        return jsonify({"success": False, "msg": str(error)}), 404

    @app.errorhandler(FollowNotFoundError)
    def handle_follow_not_found(error):
        return jsonify({"success": False, "msg": str(error)}), 404

    @app.errorhandler(TweetNotFoundError)
    def handle_tweet_not_found(error):
        return jsonify({"success": False, "msg": str(error)}), 404

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({"success": False, "msg": str(error)}), 400

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        # 可選：加上錯誤日誌紀錄
        return jsonify({"success": False, "msg": "Internal server error"}), 500
