# Owned By Sleman
# Builder pattern for creating car listings

from model.car import Car


class CarBuilder:
    def __init__(self):
        self.owner_id = None
        self.model = None
        self.year = None
        self.mileage = None
        self.pickup_location = None
        self.daily_price = None
        self.availability_calendar = []

    def set_owner(self, owner_id):
        self.owner_id = owner_id
        return self

    def set_model(self, model):
        self.model = model
        return self

    def set_year(self, year):
        self.year = int(year)
        return self

    def set_mileage(self, mileage):
        self.mileage = int(mileage)
        return self

    def set_location(self, pickup_location):
        self.pickup_location = pickup_location
        return self

    def set_price(self, daily_price):
        self.daily_price = float(daily_price)
        return self

    def set_availability(self, availability_calendar):
        self.availability_calendar = availability_calendar
        return self

    def build(self):
        if self.owner_id is None:
            raise ValueError("Owner is required")

        if self.model is None:
            raise ValueError("Model is required")

        if self.year is None:
            raise ValueError("Year is required")

        if self.mileage is None:
            raise ValueError("Mileage is required")

        if self.pickup_location is None:
            raise ValueError("Pickup location is required")

        if self.daily_price is None:
            raise ValueError("Daily price is required")

        if len(self.availability_calendar) == 0:
            raise ValueError("Availability is required")

        return Car(
            None,
            self.owner_id,
            self.model,
            self.year,
            self.mileage,
            self.pickup_location,
            self.daily_price,
            self.availability_calendar
        )