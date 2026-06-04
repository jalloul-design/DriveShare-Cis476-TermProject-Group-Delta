# Owned By Mira
# Chain Of Responsibility
import bcrypt
from model.user import User
from auth.database import get_connection

class SecurityQuestion:
    def __init__(self):
        self.next_handler = None

    def set_next_handler(self, handler):
        self.next_handler = handler
        return handler

class Question1_SecurityQuestion_Handler(SecurityQuestion):
    def handle(self, user, answer):
        if bcrypt.checkpw(answer.lower().encode(), user['security_answer_1'].encode()):
            return True, 'Correct!'
        else:
            return False, 'Incorrect!'

class Question2_SecurityQuestion_Handler(SecurityQuestion):
    def handle(self, user, answer):
        if bcrypt.checkpw(answer.lower().encode(), user['security_answer_2'].encode()):
            return True, 'Correct!'
        else:
            return False, 'Incorrect!'

class Question3_SecurityQuestion_Handler(SecurityQuestion):
    def handle(self, user, answer):
        if bcrypt.checkpw(answer.lower().encode(), user['security_answer_3'].encode()):
            return True, 'Correct! You are now able to reset your password and log back in'
        else:
            return False, 'Incorrect!'

def verify_answer(question_number, user_email, answers):
    user = User.get_user_by_email(user_email)
    if user is None:
        return False, 'Account with this email does not exist'

    # Chain
    Q1 = Question1_SecurityQuestion_Handler()
    Q2 = Question2_SecurityQuestion_Handler()
    Q3 = Question3_SecurityQuestion_Handler()
    Q1.set_next_handler(Q2)
    Q2.set_next_handler(Q3)

    current = Q1
    step = 1

    while True:
        if step == question_number:
            return current.handle(user, answers)
        if current.next_handler is None:
            return False, 'Incorrect!'
        current = current.next_handler
        step += 1

def reset_password(user_email, new_password):
    new = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET user_password = ? WHERE user_email = ?', (new, user_email))
    connection.commit()
    connection.close()
    return True, 'You have successfully reset your password'


