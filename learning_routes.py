from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from model import Learning
from db_instance import db

learning_bp = Blueprint('learning_bp', __name__)  # FIXED: matches app.py registration

@learning_bp.route('/dashboard')
@login_required
def dashboard():
    learnings = Learning.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', learnings=learnings)

@learning_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_learning():
    if request.method == 'POST':
        new_learning = Learning(
            user_id=current_user.id,
            question=request.form['question'],
            difficulty=request.form['difficulty'],
            tags=request.form['tags'],
            notes=request.form['notes'],
            link=request.form['link']
        )
        db.session.add(new_learning)
        db.session.commit()
        flash("Learning added successfully!", "success")
        return redirect(url_for('learning_bp.dashboard'))  # FIXED

    return render_template('add_learning.html')

@learning_bp.route('/delete/<int:id>')
@login_required
def delete_learning(id):
    learning = Learning.query.get_or_404(id)
    if learning.user_id != current_user.id:
        flash("You are not authorized to delete this entry.", "danger")
        return redirect(url_for('learning_bp.dashboard'))  # FIXED

    db.session.delete(learning)
    db.session.commit()
    flash("Learning deleted successfully!", "info")
    return redirect(url_for('learning_bp.dashboard'))  # FIXED
