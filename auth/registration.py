# Owned By Mira
# Function validation 
from model.user import User

def user_account_creation(user_email, user_password, questions, answers):

    if not user_email or not user_password:
        return False, "Email and password are required"

    if len(questions) != 3 or len(answers) != 3:
        return False, "You must answer all 3 questions!"

    existing = User.get_user_by_email(user_email)
    if existing is not None:
        return False, "Email is already linked to another account"

    User.create(user_email, user_password, questions, answers)
    return True, "Your account has been created!"