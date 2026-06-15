# Owned By Mohammed
# Service functions for in-app messaging.

from model.message import Message
from messaging.notification_service import NotificationService


def send_message(sender_email, recipient_email, content):
    if not sender_email:
        return False, "You must be logged in to send a message."

    if not recipient_email or not content.strip():
        return False, "Recipient and message content are required."

    message_id = Message.create(sender_email, recipient_email, content.strip())

    NotificationService.create_notification(
        recipient_email,
        "new_message",
        f"You received a new message from {sender_email}."
    )

    return True, f"Message sent successfully. Message ID: {message_id}"


def get_inbox(user_email):
    return Message.inbox_for(user_email)


def get_conversation(user1_email, user2_email):
    return Message.conversation_between(user1_email, user2_email)
