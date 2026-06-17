# Sleman Cars & Booking Module

## Overview

This is my part of the DriveShare project. I worked on the Cars & Booking section, which allows users to create car listings, search for cars, watch cars for price drops or availability changes, and book cars without double-booking the same vehicle.

## Features I Added

* Owners can create car listings with model, year, mileage, pickup location, daily price, and available dates.
* Owners can update car price and availability.
* Renters can browse all listed cars.
* Renters can search cars by location, model, dates, and price range.
* Renters can add cars to a watchlist.
* Renters can receive alerts when a watched car has a price drop or availability change.
* Renters can book cars for selected dates.
* The booking system prevents overlapping bookings for the same car.

## Design Patterns Used

### Builder Pattern

I used the Builder pattern in `cars/car_builder.py`.

The `CarBuilder` class builds a `Car` object step by step. This makes the car listing creation cleaner because a car has many fields, such as owner, model, year, mileage, location, price, and availability.

Example builder methods:

* `set_owner()`
* `set_model()`
* `set_year()`
* `set_mileage()`
* `set_location()`
* `set_price()`
* `set_availability()`
* `build()`

### Observer Pattern

I used the Observer pattern with `CarSubject` and `RenterObserver`.

The `Car` class inherits from `CarSubject`, which allows renters to watch a car. When the owner updates the car price or availability, the car notifies the renters watching it.

Main Observer files:

* `cars/car_subject.py`
* `cars/renter_observer.py`
* `model/watchlist.py`

## Files I Added

### Model Files

These files are inside the `model/` folder:

* `model/car.py`
* `model/booking.py`
* `model/watchlist.py`

### Cars Module Files

These files are inside the `cars/` folder:

* `cars/__init__.py`
* `cars/car_builder.py`
* `cars/car_subject.py`
* `cars/renter_observer.py`
* `cars/search_service.py`
* `cars/booking_service.py`
* `cars/routes.py`

### Template Files

These files are inside `auth/templates/cars/`:

* `car_list.html`
* `car_detail.html`
* `new_car.html`
* `edit_car.html`
* `search.html`
* `my_bookings.html`

### Test Files

These files are inside the `tests/` folder:

* `tests/test_cars.py`
* `tests/test_booking.py`

## UML Diagrams

I created UML diagrams for my Cars & Booking module. They are stored inside the `diagrams/` folder.

Diagrams included:

* Sleman Cars & Booking class diagram
* Builder pattern sequence diagram for creating a car listing
* Booking sequence diagram for searching and booking a car
* Observer sequence diagram for watchlist price drop notifications
* Activity diagram for the full booking process

## How the Cars Show in the App

At first, the Cars page may say that no cars have been listed yet. That is because the database is empty. Once an owner clicks “Create New Car Listing” and submits a car, the car gets saved into the database and then appears on the Browse Cars page and Search Cars page.

## How to Run Tests

From the main project folder, run:

```bash
py -m unittest discover -s tests -p "test_*.py"
```

The tests check that:

* The `CarBuilder` creates valid car objects.
* Search filters work correctly.
* The Observer pattern fires when a price drop happens.
* Valid bookings are saved.
* Overlapping bookings are blocked.

## My Main Contribution

My main contribution was building the car rental part of DriveShare. I added the logic for car listings, searching, watchlist notifications, and booking prevention. I also implemented the Builder and Observer design patterns and created the UML diagrams for my section.
