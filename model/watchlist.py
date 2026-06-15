# Owned By Sleman
# WatchListEntry class for renters watching cars

from datetime import datetime
from auth.database import get_connection


def create_watchlist_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            renter_id TEXT NOT NULL,
            car_id INTEGER NOT NULL,
            max_price REAL,
            wants_availability_alert INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()


class WatchListEntry:
    def __init__(self, id, renter_id, car_id, max_price=None, wants_availability_alert=True, created_at=None):
        self.id = id
        self.renter_id = renter_id
        self.car_id = car_id
        self.max_price = max_price
        self.wants_availability_alert = wants_availability_alert
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        create_watchlist_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO watchlist (
                renter_id,
                car_id,
                max_price,
                wants_availability_alert,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        ''', (
            self.renter_id,
            self.car_id,
            self.max_price,
            1 if self.wants_availability_alert else 0,
            self.created_at
        ))

        self.id = cursor.lastrowid

        connection.commit()
        connection.close()

    @staticmethod
    def get_watchers_by_car(car_id):
        create_watchlist_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM watchlist WHERE car_id = ?', (car_id,))
        rows = cursor.fetchall()

        connection.close()

        watchers = []

        for row in rows:
            watchers.append(WatchListEntry.from_row(row))

        return watchers

    @staticmethod
    def delete_watch(renter_id, car_id):
        create_watchlist_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            DELETE FROM watchlist
            WHERE renter_id = ?
            AND car_id = ?
        ''', (renter_id, car_id))

        connection.commit()
        connection.close()

    @staticmethod
    def from_row(row):
        return WatchListEntry(
            row["id"],
            row["renter_id"],
            row["car_id"],
            row["max_price"],
            bool(row["wants_availability_alert"]),
            row["created_at"]
        )