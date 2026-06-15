# Owned By Mohammed
# RealPaymentProcessor contains the actual payment/balance update logic.

from model.payment import Balance, Transaction


class RealPaymentProcessor:
    def process_payment(self, payer_email, payee_email, amount, booking_id=None):
        amount = float(amount)

        payer_balance = Balance.get_balance(payer_email)
        payee_balance = Balance.get_balance(payee_email)

        if amount <= 0:
            return False, "Payment amount must be greater than zero."

        if payer_balance < amount:
            Transaction.create(payer_email, payee_email, amount, booking_id, status="failed")
            return False, "Payment failed: insufficient balance."

        Balance.update_balance(payer_email, payer_balance - amount)
        Balance.update_balance(payee_email, payee_balance + amount)

        transaction_id = Transaction.create(
            payer_email,
            payee_email,
            amount,
            booking_id,
            status="completed"
        )

        return True, f"Payment successful. Transaction ID: {transaction_id}"
