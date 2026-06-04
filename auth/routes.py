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
        #Once user submits the form, this will get the values from the form
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        # Collecting the security questions from the form
        questions = [
            request.form['question1'],
            request.form['question2'],
            request.form['question3']
        ]
        # Collecting the security questions answers from the form
        answer = [
            request.form['answer1'],
            request.form['answer2'],
            request.form['answer3']
        ]

        # If successful it will create the account
        success, message = user_account_creation(user_email, user_password, questions, answer)
        flash(message)
        if success:
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Receives email and password from the form
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        # checking  if the password and email entered is valid
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
    # Shows currrent user logged in by using singleton
    session_manager = SessionManager()
    user = session_manager.get_current_user()
    return render_template('auth/homepage.html', user=user)

# Recovering account by entering their email(if user doesn't know their password)
@auth_bp.route('/recover_account', methods=['GET', 'POST'])
def recover_account():
    if request.method == 'POST':
        user_email = request.form['user_email']
        user = User.get_user_by_email(user_email)
        if user is None:
            flash('User not found with this email!')
            return render_template('auth/recover_account.html')
        return redirect(url_for('auth.recovery_questions', user_email=user_email, step=1))

    return render_template('auth/recover_account.html')

# User must answer all three security questions before creating new password( Using Chain Of Responsibility routes)
@auth_bp.route('/recovery_questions', methods=['GET', 'POST'])
def recovery_questions():
    if request.method == 'POST':
        user_email = request.form['user_email']
        step = int(request.form.get('step', 1))
        answer = request.form['answer']
    else:
        user_email = request.args.get('user_email')
        step = int(request.args.get('step', 1))
        answer = None

    user = User.get_user_by_email(user_email)
    if user is None:
        flash('User not found with this email!')
        return redirect(url_for('auth.recover_account'))

    # Displaying question on the screen
    questions_text = user[f"security_question_{step}"]

    # Verifying the user answer is correct or not
    if request.method == 'POST':
        success, message = verify_answer(step, user_email, answer)
        if not success:
            flash(message)
            return render_template('auth/recovery_questions.html',
                                   user_email=user_email, step=step,
                                   questions=questions_text)
        if step < 3:
            # If question correct, move on to the next
            return redirect(url_for('auth.recovery_questions',
                                    user_email=user_email, step=step + 1))
        else:
            # All 3 questions correct - allow password reset
            return redirect(url_for('auth.reset_password', user_email=user_email))

    return render_template('auth/recovery_questions.html',user_email=user_email, step=step, questions=questions_text)

@auth_bp.route('/reset_password', methods=['GET', 'POST'], endpoint='reset_password')
def reset_password_route():
    user_email = request.args.get('user_email')

    if request.method == 'POST':
        # Creating a new password
        new_password = request.form['new_password']
        # updates new password to the database
        success, message = reset_password(user_email, new_password)
        flash(message)
        if success:
            return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', user_email=user_email)





