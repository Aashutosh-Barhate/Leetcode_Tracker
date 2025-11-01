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


    if os.getenv("VERCEL") == "1":  
        DATABASE_URL = os.getenv("PROD_DATABASE_URL")
        if DATABASE_URL:
            app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL + "?sslmode=require"
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"poolclass": NullPool}
        else:
            raise ValueError("PROD_DATABASE_URL is not set in environment variables")
    else:  # Local development
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
    login_manager.login_view = 'auth_bp.login' 

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            print(f"Error loading user: {e}")
            return None


    from auth_routes import auth_bp
    from learning_routes import learning_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(learning_bp, url_prefix='/learning')


    @app.route('/')
    def home():
        return "Welcome to Leetcode Tracker!"


    if os.getenv("VERCEL") != "1":
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                print(f"Error creating tables locally: {e}")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=4080)
