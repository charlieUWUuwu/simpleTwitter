from flask import Flask
from app.api.users_routes import users_bp
from app.api.tweets_routes import tweets_bp
from app.api.follows_routes import follows_bp
from config import config 

app = Flask(__name__)
app.config.from_object(config["development"])

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(tweets_bp, url_prefix='/tweets')
app.register_blueprint(follows_bp, url_prefix='/follows')

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host=app.config["APP_HOST"], port=app.config["APP_PORT"])