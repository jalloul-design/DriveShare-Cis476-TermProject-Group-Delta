# Owned By Mira
# Function that will look up user by email, verification, and call session manager login

from model.user import User
from auth.session_manager import SessionManager

def login(user_email, user_password):
    user = User.verify_account(user_email, user_password)
    if user is None:
        return False, "This account does not exist, Invalid email or password"

    session_manager = SessionManager()
    session_manager.login(user['user_email'])
    return True, 'Login Successful'

def logout():
    session_manager = SessionManager()
    session_manager.logout()


