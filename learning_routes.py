from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models import Learning

# 🟢 Dashboard (View all learnings)
@app.route('/dashboard')
@login_required
def dashboard():
    learnings = Learning.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', learnings=learnings)


# 🟢 Add a new learning (GET + POST)
@app.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard'))
    return render_template('add_learning.html')


# ✏️ Delete a learning
@app.route('/delete/<int:id>')
@login_required
def delete_learning(id):
    learning = Learning.query.get_or_404(id)
    if learning.user_id != current_user.id:
        flash("You are not authorized to delete this entry.", "danger")
        return redirect(url_for('dashboard'))

    db.session.delete(learning)
    db.session.commit()
    flash("Learning deleted successfully!", "info")
    return redirect(url_for('dashboard'))
