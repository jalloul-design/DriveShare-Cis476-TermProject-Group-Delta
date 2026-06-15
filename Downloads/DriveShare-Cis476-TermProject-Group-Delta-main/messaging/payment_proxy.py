# Owned By Mohammed
# Proxy Pattern
# PaymentProxy controls access to RealPaymentProcessor.
# It checks login status, logs the request, and then forwards valid requests.

from auth.session_manager import SessionManager
from messaging.real_payment_processor import RealPaymentProcessor
from messaging.notification_service import NotificationService


class PaymentProxy:
    def __init__(self):
        self.real_processor = RealPaymentProcessor()

    def process_payment(self, payee_email, amount, booking_id=None):
        session_manager = SessionManager()
        current_user = session_manager.get_current_user()

        if current_user is None:
            return False, "Payment blocked: user must be logged in."

        print(f"[PaymentProxy] User {current_user} is attempting to pay {payee_email} ${float(amount):.2f}")

        success, message = self.real_processor.process_payment(
            payer_email=current_user,
            payee_email=payee_email,
            amount=amount,
            booking_id=booking_id
        )

        if success:
            NotificationService.create_notification(
                current_user,
                "payment_confirmation",
                f"You paid {payee_email} ${float(amount):.2f}."
            )
            NotificationService.create_notification(
                payee_email,
                "payment_received",
                f"You received ${float(amount):.2f} from {current_user}."
            )

        return success, message
