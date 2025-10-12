from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any_random_string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aashutosh:your_password@localhost/leetcode_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/')
def home():
    return "Flask + PostgreSQL connection working successfully 🚀"

if __name__ == "__main__":
    app.run(debug=True)