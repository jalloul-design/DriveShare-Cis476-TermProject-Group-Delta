# Owned By Mohammed
# Message model for in-app messaging between owners and renters.

from datetime import datetime
from auth.database import get_connection


class Message:
    def __init__(self, id=None, sender_email=None, recipient_email=None, content="", sent_at=None, read_at=None):
        self.id = id
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.content = content
        self.sent_at = sent_at or datetime.now().isoformat(timespec="seconds")
        self.read_at = read_at

    @staticmethod
    def create(sender_email, recipient_email, content):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO messages (sender_email, recipient_email, content, sent_at, read_at)
            VALUES (?, ?, ?, ?, ?)
        """, (sender_email, recipient_email, content, datetime.now().isoformat(timespec="seconds"), None))
        connection.commit()
        message_id = cursor.lastrowid
        connection.close()
        return message_id

    @staticmethod
    def inbox_for(user_email):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM messages
            WHERE recipient_email = ?
            ORDER BY sent_at DESC
        """, (user_email,))
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def conversation_between(user1_email, user2_email):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM messages
            WHERE (sender_email = ? AND recipient_email = ?)
               OR (sender_email = ? AND recipient_email = ?)
            ORDER BY sent_at ASC
        """, (user1_email, user2_email, user2_email, user1_email))
        rows = cursor.fetchall()
        connection.close()
        return rows
