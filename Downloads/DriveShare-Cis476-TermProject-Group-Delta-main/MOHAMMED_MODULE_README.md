# Mohammed Module - Messaging, Payments, Proxy, and Mediator

## Files Added

### Model files
- `model/message.py`
- `model/notification.py`
- `model/payment.py`
- `model/review.py`

### Messaging module
- `messaging/__init__.py`
- `messaging/routes.py`
- `messaging/messaging_service.py`
- `messaging/notification_service.py`
- `messaging/payment_proxy.py`
- `messaging/real_payment_processor.py`

### Mediator module
- `mediator/__init__.py`
- `mediator/ui_mediator.py`
- `mediator/components.py`

### Templates
- `auth/templates/messaging/inbox.html`
- `auth/templates/messaging/conversation.html`
- `auth/templates/messaging/notifications.html`
- `auth/templates/messaging/payment.html`
- `auth/templates/messaging/history.html`

### Tests
- `tests/test_payment.py`
- `tests/test_messaging.py`

## Design Patterns Implemented

### Proxy Pattern
`PaymentProxy` controls access to `RealPaymentProcessor`.
It checks whether the user is logged in using Mira's `SessionManager`,
logs the request, then forwards the payment to the real processor.

### Mediator Pattern
`UIMediator` allows UI/module components to communicate through one central hub.
Components do not directly reference each other.

## Routes Added
- `/messaging/messages`
- `/messaging/messages/new`
- `/messaging/notifications`
- `/messaging/pay`
- `/messaging/history`

## Database Tables Added
- `messages`
- `notifications`
- `balances`
- `transactions`
- `reviews`
