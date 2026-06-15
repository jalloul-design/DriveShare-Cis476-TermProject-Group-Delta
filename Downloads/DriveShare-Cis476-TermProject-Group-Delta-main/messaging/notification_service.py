# Owned By Mohammed
# Notification service called by messaging, payment, and other modules.

from model.notification import Notification


class NotificationService:
    @staticmethod
    def create_notification(user_email, notification_type, content):
        notification_id = Notification.create(user_email, notification_type, content)
        print(f"[NotificationService] To {user_email}: {notification_type} - {content}")
        return notification_id

    @staticmethod
    def get_notifications(user_email):
        return Notification.list_for_user(user_email)

    @staticmethod
    def mark_all_read(user_email):
        Notification.mark_all_read(user_email)
