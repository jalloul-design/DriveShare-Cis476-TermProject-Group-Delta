# Owned By Sleman
# Car class for DriveShare car listings
# This class also acts as the Subject in the Observer pattern

import json
from datetime import datetime
from auth.database import get_connection
from cars.car_subject import CarSubject


def create_car_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            mileage INTEGER NOT NULL,
            pickup_location TEXT NOT NULL,
            daily_price REAL NOT NULL,
            availability_calendar TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()


class Car(CarSubject):
    def __init__(self, id, owner_id, model, year, mileage, pickup_location, daily_price, availability_calendar, created_at=None):
        super().__init__()
        self.id = id
        self.owner_id = owner_id
        self.model = model
        self.year = year
        self.mileage = mileage
        self.pickup_location = pickup_location
        self.daily_price = daily_price
        self.availability_calendar = availability_calendar
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        create_car_table()

        connection = get_connection()
        cursor = connection.cursor()

        availability = json.dumps(self.availability_calendar)

        cursor.execute('''
            INSERT INTO cars (
                owner_id,
                model,
                year,
                mileage,
                pickup_location,
                daily_price,
                availability_calendar,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.owner_id,
            self.model,
            self.year,
            self.mileage,
            self.pickup_location,
            self.daily_price,
            availability,
            self.created_at
        ))

        self.id = cursor.lastrowid

        connection.commit()
        connection.close()

    def update_price(self, new_price):
        old_price = self.daily_price
        self.daily_price = float(new_price)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            UPDATE cars
            SET daily_price = ?
            WHERE id = ?
        ''', (self.daily_price, self.id))

        connection.commit()
        connection.close()

        if self.daily_price < old_price:
            self.notify("price_drop", {
                "car_id": self.id,
                "model": self.model,
                "old_price": old_price,
                "new_price": self.daily_price
            })

    def update_availability(self, availability_calendar):
        self.availability_calendar = availability_calendar

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            UPDATE cars
            SET availability_calendar = ?
            WHERE id = ?
        ''', (json.dumps(self.availability_calendar), self.id))

        connection.commit()
        connection.close()

        self.notify("availability_change", {
            "car_id": self.id,
            "model": self.model,
            "availability_calendar": self.availability_calendar
        })

    def is_available_for_dates(self, start_date, end_date):
        if start_date >= end_date:
            return False

        available = False

        for date_range in self.availability_calendar:
            available_start = date_range["start"]
            available_end = date_range["end"]

            if start_date >= available_start and end_date <= available_end:
                available = True

        if not available:
            return False

        from model.booking import Booking

        if Booking.check_overlap(self.id, start_date, end_date):
            return False

        return True

    @staticmethod
    def get_all_cars():
        create_car_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM cars')
        rows = cursor.fetchall()

        connection.close()

        cars = []

        for row in rows:
            cars.append(Car.from_row(row))

        return cars

    @staticmethod
    def get_car_by_id(car_id):
        create_car_table()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM cars WHERE id = ?', (car_id,))
        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return Car.from_row(row)

    @staticmethod
    def from_row(row):
        availability = json.loads(row["availability_calendar"])

        return Car(
            row["id"],
            row["owner_id"],
            row["model"],
            row["year"],
            row["mileage"],
            row["pickup_location"],
            row["daily_price"],
            availability,
            row["created_at"]
        )