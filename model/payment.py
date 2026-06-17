# Owned By Mohammed
# Balance and Transaction models used by the Proxy payment flow.

from datetime import datetime
from auth.database import get_connection


def create_payment_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS balances (
            user_email TEXT PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payer_email TEXT NOT NULL,
            payee_email TEXT NOT NULL,
            amount REAL NOT NULL,
            booking_id INTEGER,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


class Balance:
    @staticmethod
    def create_if_missing(user_email, starting_balance=1000.00):
        create_payment_tables()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM balances WHERE user_email = ?", (user_email,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                "INSERT INTO balances (user_email, amount) VALUES (?, ?)",
                (user_email, float(starting_balance))
            )
            connection.commit()

        connection.close()

    @staticmethod
    def get_balance(user_email):
        create_payment_tables()

        Balance.create_if_missing(user_email)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT amount FROM balances WHERE user_email = ?", (user_email,))
        row = cursor.fetchone()

        connection.close()

        return float(row["amount"]) if row else 0.0

    @staticmethod
    def update_balance(user_email, new_amount):
        create_payment_tables()

        Balance.create_if_missing(user_email)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE balances SET amount = ? WHERE user_email = ?",
            (float(new_amount), user_email)
        )

        connection.commit()
        connection.close()


class Transaction:
    @staticmethod
    def create(payer_email, payee_email, amount, booking_id=None, status="completed"):
        create_payment_tables()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO transactions (
                payer_email,
                payee_email,
                amount,
                booking_id,
                status,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            payer_email,
            payee_email,
            float(amount),
            booking_id,
            status,
            datetime.now().isoformat(timespec="seconds")
        ))

        connection.commit()

        transaction_id = cursor.lastrowid

        connection.close()

        return transaction_id

    @staticmethod
    def list_for_user(user_email):
        create_payment_tables()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM transactions
            WHERE payer_email = ?
            OR payee_email = ?
            ORDER BY timestamp DESC
        """, (user_email, user_email))

        rows = cursor.fetchall()

        connection.close()

        return rows