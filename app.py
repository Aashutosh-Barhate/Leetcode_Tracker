from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from db_instance import db
from model import User, Learning

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'any_random_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leetuser:2705@localhost/leetcode_tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from auth_routes import auth_bp
    from learning_routes import learning_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(learning_bp, url_prefix='/learning')

    # Home route
    @app.route('/')
    def home():
        return "Welcome to Leetcode Tracker!"

    return app

# Run only if this file is executed directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=4080)
