# Owned By Mohammed
# Notification model for booking, payment, message, and price-drop alerts.

from datetime import datetime
from auth.database import get_connection


def create_notification_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            notification_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            read INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


class Notification:
    def __init__(self, id=None, user_email=None, notification_type="", content="", created_at=None, read=False):
        self.id = id
        self.user_email = user_email
        self.notification_type = notification_type
        self.content = content
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self.read = read

    @staticmethod
    def create(user_email, notification_type, content):
        create_notification_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO notifications (
                user_email,
                notification_type,
                content,
                created_at,
                read
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_email,
            notification_type,
            content,
            datetime.now().isoformat(timespec="seconds"),
            0
        ))

        connection.commit()

        notification_id = cursor.lastrowid

        connection.close()

        return notification_id

    @staticmethod
    def list_for_user(user_email):
        create_notification_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM notifications
            WHERE user_email = ?
            ORDER BY created_at DESC
        """, (user_email,))

        rows = cursor.fetchall()

        connection.close()

        return rows

    @staticmethod
    def mark_all_read(user_email):
        create_notification_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE notifications
            SET read = 1
            WHERE user_email = ?
        """, (user_email,))

        connection.commit()
        connection.close()