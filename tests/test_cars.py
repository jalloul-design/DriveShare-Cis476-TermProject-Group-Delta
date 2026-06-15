# Owned By Sleman
# Unit tests for CarBuilder, search, and Observer

import os
import unittest

from model.car import create_car_table
from cars.car_builder import CarBuilder
from cars.search_service import search_cars


class TestCars(unittest.TestCase):
    def setUp(self):
        if os.path.exists("driveshare.db"):
            os.remove("driveshare.db")

        create_car_table()

    def test_car_builder_creates_valid_car(self):
        car = CarBuilder() \
            .set_owner("owner@test.com") \
            .set_model("Honda Civic") \
            .set_year(2020) \
            .set_mileage(50000) \
            .set_location("Dearborn") \
            .set_price(60) \
            .set_availability([
                {
                    "start": "2026-06-20",
                    "end": "2026-06-30"
                }
            ]) \
            .build()

        self.assertEqual(car.model, "Honda Civic")
        self.assertEqual(car.owner_id, "owner@test.com")
        self.assertEqual(car.daily_price, 60)

    def test_search_filters_work(self):
        car = CarBuilder() \
            .set_owner("owner@test.com") \
            .set_model("Toyota Camry") \
            .set_year(2021) \
            .set_mileage(30000) \
            .set_location("Dearborn") \
            .set_price(75) \
            .set_availability([
                {
                    "start": "2026-06-20",
                    "end": "2026-06-30"
                }
            ]) \
            .build()

        car.save()

        results = search_cars(
            location="Dearborn",
            min_price="50",
            max_price="100",
            model="Toyota"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].model, "Toyota Camry")

    def test_observer_fires_on_price_drop(self):
        car = CarBuilder() \
            .set_owner("owner@test.com") \
            .set_model("Tesla Model 3") \
            .set_year(2022) \
            .set_mileage(20000) \
            .set_location("Detroit") \
            .set_price(100) \
            .set_availability([
                {
                    "start": "2026-06-20",
                    "end": "2026-06-30"
                }
            ]) \
            .build()

        events = []

        class FakeObserver:
            def update(self, event_type, data):
                events.append(event_type)

        car.attach(FakeObserver())

        car.notify("price_drop", {
            "car_id": 1,
            "model": "Tesla Model 3",
            "old_price": 100,
            "new_price": 80
        })

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0], "price_drop")


if __name__ == "__main__":
    unittest.main()