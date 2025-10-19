from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from auth_routes import auth_bp
from learning_routes import learning_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any_random_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leetuser:2705@localhost/leetcode_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  

from auth_routes import *
from learning_routes import *
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(learning_bp, url_prefix="/learning")


from model import *
with app.app_context():
    db.create_all()
app.run(debug=True)
