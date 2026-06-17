# DriveShare-Cis476-TermProject-Group-Delta

DriveShare is a peer-to-peer car rental platform inspired by Turo, built in Python with Flask and SQLite. Users can register an account (secured with bcrypt hashing and three security questions for recovery), log in, and access three connected modules: auth for sessions and accounts, cars for listings, search, booking with overlap prevention, and watchlist alerts, and messaging for in-app messages, notifications, and payments. The project implements all six required design patterns which are Singleton, Chain of Responsibility, Builder, Observer, Proxy, and Mediator, distributed across the three person group. Each module communicates through a shared SessionManager Singleton, allowing renters and owners to list cars, book trips, message each other, and complete payments in one seamless flow.

## Team Members

- Mira Jalloul
- Sleman Ahmed
- Mohammed Nour

## Tech Stack

- **Python 3**
- **Flask** (web framework with Blueprints)
- **SQLite** (file-based database)
- **bcrypt** (password and security answer hashing)
- **Jinja2** (HTML templates)

## Features

- User registration with three security questions
- Login and logout with bcrypt password verification
- Password recovery through security questions
- Car listing creation and management
- Car search with multiple filters
- Booking with date overlap prevention
- Watchlist with availability and price drop alerts
- In-app messaging between users
- Payment simulation with balance updates
- Notifications for booking events
- Rental history and transaction log

## How to Run

From the project terminal:
pip install -r requirements.txt
python app.py

## Test flow

1. Register an account at /register — choose 3 security questions and write down the answers
2. Log in at /login
3. Land on /homepage with the navigation menu
4. List a car, search for cars, book one, send a message, make a payment
5. Test password recovery by logging out and clicking "Forgot Password"

## Presentation URL
Slides: https://umich-my.sharepoint.com/:p:/g/personal/jalloul_umich_edu/IQBX0sXmBWC2TLll3aT3OjcqAavRk9ePVS04VjmDI8tptYk?e=mMc7kC

# Mira Module - Authentication, Sessions, Singleton, and Chain of Responsibility

## Files Added

## Model files

- `model/user.py`


## Auth module

- `auth/__init__.py`

- `auth/routes.py`

- `auth/session_manager.py`

- `auth/registration.py`

- `auth/login.py`

- `auth/password_recovery.py`


## Foundation files

- `app.py`

- `database.py`

- `requirements.txt`


## Templates

- `templates/auth/register.html`

- `templates/auth/login.html`

- `templates/auth/homepage.html`

- `templates/auth/recover_account.html`

- `templates/auth/recovery_questions.html`

- `templates/auth/reset_password.html`


## Tests

- `tests/test_auth.py`

## Design Patterns Implemented

- Singleton Pattern
SessionManager ensures only one instance exists across the entire application. It tracks the user crurrently logged so any module like  auth, cars, messaging can check the session through the same shared object.

- Chain of Responsibility Pattern
SecurityQuestion is the base handler. Three handlers which are Question1_SecurityQuestion_Handler, Question2_SecurityQuestion_Handler, Question3_SecurityQuestion_Handler are all linked together. The user must pass all three questions in order to move forward and reset their password.

## Routes Added

- `/register`

- `/login`

- `/logout`

- `/homepage`

- `/recover_account`

- `/recovery_questions`

- `/reset_password`


## Database Tables Added

- `users`

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
