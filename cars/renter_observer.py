# Owned By Sleman
# Observer class for renters watching a car

import importlib


class RenterObserver:
    def __init__(self, renter_id, max_price=None, wants_availability_alert=True):
        self.renter_id = renter_id
        self.max_price = max_price
        self.wants_availability_alert = wants_availability_alert

    def update(self, event_type, data):
        if event_type == "price_drop":
            new_price = data["new_price"]

            if self.max_price is not None and new_price > self.max_price:
                return

            message = "Price drop alert: " + data["model"] + " is now $" + str(new_price)

            self.send_notification("price_drop", message)

        elif event_type == "availability_change":
            if self.wants_availability_alert:
                message = "Availability alert: " + data["model"] + " has updated availability"

                self.send_notification("availability_change", message)

    def send_notification(self, notification_type, message):
        try:
            notification_module = importlib.import_module("messaging.notification_service")
            NotificationService = notification_module.NotificationService

            NotificationService.create_notification(
                self.renter_id,
                notification_type,
                message
            )

        except:
            print("Notification for " + str(self.renter_id) + ": " + message)