# Owned By Mira
# Defines User Fields like password,email,id number, etc
import bcrypt
from database import get_connection

class User:
    def __init__(self, id, user_email, user_password):
        self.id = id
        self.user_email = user_email
        self.user_password = user_password

    @staticmethod
    def create_account(user_email, user_password, questions, answers):

        # Hashing the password
        hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()

        # Hashing all 3 answers
        answer1 = bcrypt.hashpw(answers[0].lower().encode(), bcrypt.gensalt()).decode()
        answer2 = bcrypt.hashpw(answers[1].lower().encode(), bcrypt.gensalt()).decode()
        answer3 = bcrypt.hashpw(answers[2].lower().encode(), bcrypt.gensalt()).decode()

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO users (user_email, user_password,
                security_question_1, security_answer_1,
                security_question_2, security_answer_2,
                security_question_3, security_answer_3)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_email, hashed_password,
              questions[0], answer1,
              questions[1], answer2,
              questions[2], answer3))
        connection.commit()
        connection.close()

    @staticmethod
    def get_user_by_email(user_email):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_email = ?', (user_email,))
        row = cursor.fetchone()
        connection.close()
        return row

    @staticmethod
    def verify_account(user_email, user_password):
        user = User.get_user_by_email(user_email)
        if user is None:
            return None

        if bcrypt.checkpw(user_password.encode(), user['user_password'].encode()):
            return user
        else:
            return None




