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


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email TEXT NOT NULL,
            recipient_email TEXT NOT NULL,
            content TEXT NOT NULL,
            sent_at TEXT NOT NULL,
            read_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            notification_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            read INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT UNIQUE NOT NULL,
            amount REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payer_email TEXT NOT NULL,
            payee_email TEXT NOT NULL,
            amount REAL NOT NULL,
            booking_id TEXT,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reviewer_email TEXT NOT NULL,
            reviewee_email TEXT NOT NULL,
            booking_id TEXT,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
