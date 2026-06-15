# Owned By Sleman
# Search service for filtering cars

from model.car import Car


def search_cars(location=None, start_date=None, end_date=None, min_price=None, max_price=None, model=None):
    cars = Car.get_all_cars()
    results = []

    for car in cars:
        if location:
            if location.lower() not in car.pickup_location.lower():
                continue

        if model:
            if model.lower() not in car.model.lower():
                continue

        if min_price:
            if car.daily_price < float(min_price):
                continue

        if max_price:
            if car.daily_price > float(max_price):
                continue

        if start_date and end_date:
            if not car.is_available_for_dates(start_date, end_date):
                continue

        results.append(car)

    return results