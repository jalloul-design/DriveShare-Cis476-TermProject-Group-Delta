# Owned By Mohammed
# Flask Blueprint routes for messages, notifications, payments, and history.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth.session_manager import SessionManager
from messaging.messaging_service import send_message, get_inbox, get_conversation
from messaging.notification_service import NotificationService
from messaging.payment_proxy import PaymentProxy
from model.notification import Notification
from model.payment import Balance, Transaction

messaging_bp = Blueprint("messaging", __name__, url_prefix="/messaging")


def current_user_email():
    return SessionManager().get_current_user()


@messaging_bp.route("/messages")
def messages():
    user = current_user_email()

    if user is None:
        flash("Please log in first.")
        return redirect(url_for("auth.login"))

    inbox = get_inbox(user)

    return render_template("messaging/inbox.html", user=user, inbox=inbox)


@messaging_bp.route("/messages/new", methods=["GET", "POST"])
def new_message():
    user = current_user_email()

    if user is None:
        flash("Please log in first.")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        recipient_email = request.form["recipient_email"]
        content = request.form["content"]

        success, message = send_message(user, recipient_email, content)
        flash(message)

        if success:
            return redirect(url_for("messaging.messages"))

    return render_template("messaging/conversation.html", user=user)


@messaging_bp.route("/messages/conversation/<recipient_email>")
def conversation(recipient_email):
    user = current_user_email()

    if user is None:
        flash("Please log in first.")
        return redirect(url_for("auth.login"))

    messages = get_conversation(user, recipient_email)

    return render_template(
        "messaging/conversation.html",
        user=user,
        recipient_email=recipient_email,
        messages=messages
    )


@messaging_bp.route("/notifications")
def notifications():
    user = current_user_email()

    if user is None:
        flash("Please log in first.")
        return redirect(url_for("auth.login"))

    Notification.mark_all_read(user)

    items = NotificationService.get_notifications(user)

    return render_template("messaging/notifications.html", user=user, notifications=items)


@messaging_bp.route("/pay", methods=["GET", "POST"])
def pay():
    user = current_user_email()

    if user is None:
        flash("Please log in first.")
        return redirect(url_for("auth.login"))

    Balance.create_if_missing(user)

    prefill_payee_email = request.args.get("payee_email", "")
    prefill_amount = request.args.get("amount", "")
    prefill_booking_id = request.args.get("booking_id", "")

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_funds" or "fund_amount" in request.form:
            fund_amount = float(request.form.get("fund_amount", 0))

            if fund_amount <= 0:
                flash("Amount must be greater than zero.")
                return redirect(url_for("messaging.pay"))

            current_balance = Balance.get_balance(user)
            new_balance = current_balance + fund_amount

            Balance.update_balance(user, new_balance)

            flash("Funds added successfully.")
            return redirect(url_for("messaging.pay"))

        payee_email = request.form.get("payee_email")
        amount = request.form.get("amount")
        booking_id = request.form.get("booking_id") or None

        if not payee_email or not amount:
            flash("Payee email and amount are required.")
            return redirect(url_for("messaging.pay"))

        proxy = PaymentProxy()
        success, message = proxy.process_payment(payee_email, amount, booking_id)

        if success:
            flash(message)
            flash("Payment received and recorded.")
            return redirect(url_for("messaging.history"))

        flash(message)

    balance = Balance.get_balance(user)

    return render_template(
        "messaging/payment.html",
        user=user,
        balance=balance,
        prefill_payee_email=prefill_payee_email,
        prefill_amount=prefill_amount,
        prefill_booking_id=prefill_booking_id
    )


@messaging_bp.route("/history")
def history():
    user = current_user_email()

    if user is None:
        flash("Please log in first.")
        return redirect(url_for("auth.login"))

    transactions = Transaction.list_for_user(user)
    balance = Balance.get_balance(user)

    return render_template(
        "messaging/history.html",
        user=user,
        transactions=transactions,
        balance=balance
    )