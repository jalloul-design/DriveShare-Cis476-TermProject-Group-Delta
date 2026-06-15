# Owned By Sleman
# Booking logic with overlap prevention

from datetime import datetime
from model.car import Car
from model.booking import Booking


def create_booking(car_id, renter_id, start_date, end_date):
    car = Car.get_car_by_id(car_id)

    if car is None:
        return False, "Car not found"

    if start_date >= end_date:
        return False, "End date must be after start date"

    if not car.is_available_for_dates(start_date, end_date):
        return False, "Car is not available or already booked for these dates"

    if Booking.check_overlap(car_id, start_date, end_date):
        return False, "This car is already booked for these dates"

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days

    total_price = days * car.daily_price

    booking = Booking(
        None,
        car_id,
        renter_id,
        start_date,
        end_date,
        total_price,
        "confirmed"
    )

    booking.save()

    return True, "Booking confirmed"