from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from db_instance import db
from model import User, Learning
from flask_cors import CORS
from dotenv import load_dotenv
import os
from sqlalchemy.pool import NullPool

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # Determine environment
    if os.getenv("VERCEL") == "1":  # Running on Vercel
        DATABASE_URL = os.getenv("PROD_DATABASE_URL")
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL + "?sslmode=require"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"poolclass": NullPool}  # Prevent serverless DB drops
    else:  # Local
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

    db.init_app(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth_routes import auth_bp
    from learning_routes import learning_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(learning_bp, url_prefix='/learning')

    @app.route('/')
    def home():
        return "Welcome to Leetcode Tracker!"

    # Only create tables locally
    if os.getenv("VERCEL") != "1":
        with app.app_context():
            db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=4080)
