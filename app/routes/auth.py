from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import Member

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if Member.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.register'))
        if Member.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('auth.register'))
        member = Member(username=username, email=email)
        member.set_password(password)
        db.session.add(member)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        member = Member.query.filter_by(username=username).first()
        if member and member.check_password(password):
            if not member.is_active_member:
                flash('Your account has been deactivated', 'error')
                return redirect(url_for('auth.login'))
            login_user(member)
            return redirect(url_for('main.index'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', '')
        current_user.phone = request.form.get('phone', '')
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('auth.profile'))
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/deactivate', methods=['POST'])
@login_required
def deactivate():
    current_user.deactivate()
    db.session.commit()
    logout_user()
    flash('Your account has been deactivated', 'info')
    return redirect(url_for('auth.login'))
