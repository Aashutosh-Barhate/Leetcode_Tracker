from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from db_instance import db
from model import User, Learning
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load local .env for development
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # SECRET KEY
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # DATABASE CONFIG
    DATABASE_URL = os.getenv("PROD_DATABASE_URL")
    if DATABASE_URL:
        # Production (Vercel) — add SSL for PostgreSQL
        if "?" not in DATABASE_URL:
            DATABASE_URL += "?sslmode=require"
        else:
            DATABASE_URL += "&sslmode=require"
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        print("✅ Running in PRODUCTION mode (Vercel)")
    else:
        # Local development
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        print("💻 Running in LOCAL mode")

    # INIT DB
    db.init_app(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # REGISTER BLUEPRINTS
    from auth_routes import auth_bp
    from learning_routes import learning_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(learning_bp, url_prefix='/learning')

    # HOME ROUTE
    @app.route('/')
    def home():
        return "Welcome to Leetcode Tracker!"

    # CREATE TABLES AUTOMATICALLY
    with app.app_context():
        try:
            db.create_all()
            print("🧱 Database tables checked/created successfully!")
        except Exception as e:
            print("⚠️ Error creating tables:", e)

    return app

if __name__ == '__main__':
    app = create_app()
    # Run locally on port 4080
    app.run(debug=True, port=4080)
