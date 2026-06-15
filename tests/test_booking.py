# Owned By Sleman
# Unit tests for booking overlap prevention

import os
import unittest

from model.car import create_car_table
from model.booking import create_booking_table
from cars.car_builder import CarBuilder
from cars.booking_service import create_booking


class TestBooking(unittest.TestCase):
    def setUp(self):
        if os.path.exists("driveshare.db"):
            os.remove("driveshare.db")

        create_car_table()
        create_booking_table()

        self.car = CarBuilder() \
            .set_owner("owner@test.com") \
            .set_model("Honda Accord") \
            .set_year(2021) \
            .set_mileage(25000) \
            .set_location("Dearborn") \
            .set_price(60) \
            .set_availability([
                {
                    "start": "2026-06-20",
                    "end": "2026-06-30"
                }
            ]) \
            .build()

        self.car.save()

    def test_valid_booking_saves_correctly(self):
        success, message = create_booking(
            self.car.id,
            "renter@test.com",
            "2026-06-21",
            "2026-06-23"
        )

        self.assertTrue(success)
        self.assertEqual(message, "Booking confirmed")

    def test_overlap_booking_is_blocked(self):
        create_booking(
            self.car.id,
            "renter1@test.com",
            "2026-06-21",
            "2026-06-24"
        )

        success, message = create_booking(
            self.car.id,
            "renter2@test.com",
            "2026-06-22",
            "2026-06-25"
        )

        self.assertFalse(success)
        self.assertIn("not available", message)


if __name__ == "__main__":
    unittest.main()