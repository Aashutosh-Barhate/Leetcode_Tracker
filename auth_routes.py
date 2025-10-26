from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from model import User
from db_instance import db

auth_bp = Blueprint('auth_bp', __name__)  # FIXED: blueprint name matches app.py

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('auth_bp.signup'))  # FIXED: use blueprint endpoint

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please login.", "success")
        return redirect(url_for('auth_bp.login'))  # FIXED

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials, please try again.", "danger")
            return redirect(url_for('auth_bp.login'))  # FIXED

        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for('learning_bp.dashboard'))  # Assuming your learning blueprint is correct

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth_bp.login'))  # FIXED
