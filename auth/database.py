import sqlite3

def get_connection():
    connection = sqlite3.connect('driveshare.db')
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT UNIQUE NOT NULL,
            user_password TEXT NOT NULL,
            security_question_1 TEXT NOT NULL,
            security_answer_1 TEXT NOT NULL,
            security_question_2 TEXT NOT NULL,
            security_answer_2 TEXT NOT NULL,
            security_question_3 TEXT NOT NULL,
            security_answer_3 TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()
