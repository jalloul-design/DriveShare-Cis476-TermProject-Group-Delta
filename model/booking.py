# Owned By Sleman
# Booking class for saving rentals and stopping double bookings


from datetime import datetime
from auth.database import get_connection

def create_booking_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER NOT NULL,
            renter_id TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()


class Booking:
    def __init__(self, id, car_id, renter_id, start_date, end_date, total_price, status="confirmed", created_at=None):
        self.id = id
        self.car_id = car_id
        self.renter_id = renter_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        create_booking_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO bookings (
                car_id,
                renter_id,
                start_date,
                end_date,
                total_price,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.car_id,
            self.renter_id,
            self.start_date,
            self.end_date,
            self.total_price,
            self.status,
            self.created_at
        ))

        self.id = cursor.lastrowid

        connection.commit()
        connection.close()

    @staticmethod
    def check_overlap(car_id, start, end):
        create_booking_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT * FROM bookings
            WHERE car_id = ?
            AND status != 'cancelled'
        ''', (car_id,))

        rows = cursor.fetchall()

        connection.close()

        for row in rows:
            existing_start = row["start_date"]
            existing_end = row["end_date"]

            if start < existing_end and end > existing_start:
                return True

        return False

    @staticmethod
    def get_bookings_by_renter(renter_id):
        create_booking_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM bookings WHERE renter_id = ?', (renter_id,))
        rows = cursor.fetchall()

        connection.close()

        bookings = []

        for row in rows:
            bookings.append(Booking.from_row(row))

        return bookings

    @staticmethod
    def from_row(row):
        return Booking(
            row["id"],
            row["car_id"],
            row["renter_id"],
            row["start_date"],
            row["end_date"],
            row["total_price"],
            row["status"],
            row["created_at"]
        )