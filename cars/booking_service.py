# Owned By Sleman
# Booking service for checking availability and creating bookings

import json
from datetime import datetime
from model.car import Car
from model.booking import Booking


def convert_availability(availability):
    if availability is None:
        return []

    if isinstance(availability, list):
        return availability

    if isinstance(availability, str):
        try:
            return json.loads(availability)
        except:
            return []

    return []


def get_car_availability(car):
    if hasattr(car, "availability_calendar"):
        return convert_availability(car.availability_calendar)

    if hasattr(car, "availability"):
        return convert_availability(car.availability)

    return []


def car_is_available(car, start_date, end_date):
    availability = get_car_availability(car)

    for available_range in availability:
        available_start = available_range["start"]
        available_end = available_range["end"]

        if start_date >= available_start and end_date <= available_end:
            return True

    return False


def create_booking(car_id, renter_id, start_date, end_date):
    car = Car.get_car_by_id(car_id)

    if car is None:
        return False, "Car not found"

    if start_date >= end_date:
        return False, "End date must be after start date"

    if not car_is_available(car, start_date, end_date):
        return False, "Car is not available for these dates"

    if Booking.check_overlap(car_id, start_date, end_date):
        return False, "Car is already booked for these dates"

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days

    total_price = days * float(car.daily_price)

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

    return True, "Booking created successfully"