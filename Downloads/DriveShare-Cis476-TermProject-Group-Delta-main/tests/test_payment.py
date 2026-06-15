# Owned By Mohammed
# Basic tests for the PaymentProxy pattern.

from auth.session_manager import SessionManager
from messaging.payment_proxy import PaymentProxy


def test_payment_proxy_blocks_logged_out_user():
    session = SessionManager()
    session.logout()

    proxy = PaymentProxy()
    success, message = proxy.process_payment("owner@test.com", 100)

    assert success is False
    assert "logged in" in message.lower()


def test_session_manager_singleton_used_by_payment_proxy():
    session1 = SessionManager()
    session2 = SessionManager()

    assert session1 is session2
