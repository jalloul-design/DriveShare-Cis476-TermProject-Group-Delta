# Owned By Mira
# Flask Routes that tie everything together

from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth.registration import user_account_creation
from auth.login import user_login, user_logout
from auth.session_manager import SessionManager
from auth.password_recovery import verify_answer, reset_password
from model.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        questions = [
            request.form['question1'],
            request.form['question2'],
            request.form['question3']
        ]
        answer = [
            request.form['answer1'],
            request.form['answer2'],
            request.form['answer3']
        ]

        success, message = user_account_creation(user_email, user_password, questions, answer)
        flash(message)
        if success:
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        success, message = user_login(user_email, user_password)
        flash(message)
        if success:
            return redirect(url_for('auth.homepage'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    user_logout()
    flash('You have been logged out!')
    return redirect(url_for('auth.login'))


@auth_bp.route('/homepage')
def homepage():
    session_manager = SessionManager()
    user = session_manager.get_current_user()
    return render_template('auth/homepage.html', user=user)





