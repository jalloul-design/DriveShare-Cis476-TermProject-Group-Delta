# DriveShare-Cis476-TermProject-Group-Delta
- DriveShare is a peer-to-peer car rental platform inspired by Turo, built in Python with Flask and SQLite. Users can register an account (secured with bcrypt hashing and three security questions for recovery), log in, and access three connected modules: auth for sessions and accounts, cars for listings, search, booking with overlap prevention, and watchlist alerts, and messaging for in-app messages, notifications, and payments. The project implements all six required design patterns which are Singleton, Chain of Responsibility, Builder, Observer, Proxy, and Mediator, distributed across the three person group. Each module communicates through a shared SessionManager Singleton, allowing renters and owners to list cars, book trips, message each other, and complete payments in one seamless flow.

# Mira Module - Authentication, Sessions, Singleton, and Chain of Responsibility

# Files Added

# Model files

- model/user.py


# Auth module

- auth/__init__.py

- auth/routes.py

- auth/session_manager.py

- auth/registration.py

- auth/login.py

- auth/password_recovery.py


# Foundation files

- app.py

- database.py

- requirements.txt


# Templates

- templates/auth/register.html

- templates/auth/login.html

- templates/auth/homepage.html

- templates/auth/recover_account.html

- templates/auth/recovery_questions.html

- templates/auth/reset_password.html


# Tests

- tests/test_auth.py

# Design Patterns Implemented

- Singleton Pattern
SessionManager ensures only one instance exists across the entire application. It tracks the user crurrently logged so any module like  auth, cars, messaging can check the session through the same shared object.

- Chain of Responsibility Pattern
SecurityQuestion is the base handler. Three handlers which are Question1_SecurityQuestion_Handler, Question2_SecurityQuestion_Handler, Question3_SecurityQuestion_Handler are all linked together. The user must pass all three questions in order to move forward and reset their password.

# Routes Added

- /register

- /login

- /logout

- /homepage

- /recover_account

- /recovery_questions

- /reset_password


# Database Tables Added

- users
