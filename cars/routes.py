# Owned By Sleman
# Routes for car listings, search, watchlist, and booking

from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth.session_manager import SessionManager
from cars.car_builder import CarBuilder
from cars.search_service import search_cars
from cars.booking_service import create_booking
from cars.renter_observer import RenterObserver
from model.car import Car
from model.booking import Booking
from model.watchlist import WatchListEntry

cars_bp = Blueprint("cars", __name__)


def get_current_user():
    session_manager = SessionManager()
    return session_manager.get_current_user()


def users_match(user_one, user_two):
    if user_one is None or user_two is None:
        return False

    return str(user_one).strip().lower() == str(user_two).strip().lower()


@cars_bp.route("/cars")
def cars():
    all_cars = Car.get_all_cars()
    return render_template("cars/car_list.html", cars=all_cars)


@cars_bp.route("/cars/new", methods=["GET", "POST"])
def new_car():
    current_user = get_current_user()

    if current_user is None:
        flash("You must be logged in first")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        availability = [
            {
                "start": request.form["availability_start"],
                "end": request.form["availability_end"]
            }
        ]

        try:
            car = CarBuilder() \
                .set_owner(current_user) \
                .set_model(request.form["model"]) \
                .set_year(request.form["year"]) \
                .set_mileage(request.form["mileage"]) \
                .set_location(request.form["pickup_location"]) \
                .set_price(request.form["daily_price"]) \
                .set_availability(availability) \
                .build()

            car.save()

            flash("Car listing created")
            return redirect(url_for("cars.car_detail", car_id=car.id))

        except Exception as error:
            flash(str(error))

    return render_template("cars/new_car.html")


@cars_bp.route("/cars/<int:car_id>")
def car_detail(car_id):
    current_user = get_current_user()
    car = Car.get_car_by_id(car_id)

    if car is None:
        flash("Car not found")
        return redirect(url_for("cars.cars"))

    is_owner = users_match(current_user, car.owner_id)

    return render_template(
        "cars/car_detail.html",
        car=car,
        current_user=current_user,
        is_owner=is_owner
    )


@cars_bp.route("/cars/<int:car_id>/edit", methods=["GET", "POST"])
def edit_car(car_id):
    current_user = get_current_user()
    car = Car.get_car_by_id(car_id)

    if current_user is None:
        flash("You must be logged in first")
        return redirect(url_for("auth.login"))

    if car is None:
        flash("Car not found")
        return redirect(url_for("cars.cars"))

    if not users_match(car.owner_id, current_user):
        flash("Only the owner can edit this car")
        return redirect(url_for("cars.car_detail", car_id=car.id))

    if request.method == "POST":
        watchers = WatchListEntry.get_watchers_by_car(car.id)

        for watcher in watchers:
            observer = RenterObserver(
                watcher.renter_id,
                watcher.max_price,
                watcher.wants_availability_alert
            )

            car.attach(observer)

        availability = [
            {
                "start": request.form["availability_start"],
                "end": request.form["availability_end"]
            }
        ]

        car.update_price(request.form["daily_price"])
        car.update_availability(availability)

        flash("Car updated")
        return redirect(url_for("cars.car_detail", car_id=car.id))

    return render_template("cars/edit_car.html", car=car)


@cars_bp.route("/search")
def search():
    results = search_cars(
        request.args.get("location"),
        request.args.get("start_date"),
        request.args.get("end_date"),
        request.args.get("min_price"),
        request.args.get("max_price"),
        request.args.get("model")
    )

    return render_template("cars/search.html", cars=results)


@cars_bp.route("/watch/<int:car_id>", methods=["POST"])
def watch_car(car_id):
    current_user = get_current_user()

    if current_user is None:
        flash("You must be logged in first")
        return redirect(url_for("auth.login"))

    car = Car.get_car_by_id(car_id)

    if car is None:
        flash("Car not found")
        return redirect(url_for("cars.cars"))

    if users_match(car.owner_id, current_user):
        flash("You cannot watch your own car")
        return redirect(url_for("cars.car_detail", car_id=car_id))

    max_price = request.form.get("max_price")
    wants_availability_alert = request.form.get("wants_availability_alert") == "on"

    watch = WatchListEntry(
        None,
        current_user,
        car_id,
        max_price,
        wants_availability_alert
    )

    watch.save()

    flash("Car added to watchlist")
    return redirect(url_for("cars.car_detail", car_id=car_id))


@cars_bp.route("/unwatch/<int:car_id>", methods=["POST"])
def unwatch_car(car_id):
    current_user = get_current_user()

    if current_user is None:
        flash("You must be logged in first")
        return redirect(url_for("auth.login"))

    WatchListEntry.delete_watch(current_user, car_id)

    flash("Car removed from watchlist")
    return redirect(url_for("cars.car_detail", car_id=car_id))


@cars_bp.route("/book", methods=["POST"])
def book():
    current_user = get_current_user()

    if current_user is None:
        flash("You must be logged in first")
        return redirect(url_for("auth.login"))

    car_id = request.form["car_id"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]

    car = Car.get_car_by_id(car_id)

    if car is None:
        flash("Car not found")
        return redirect(url_for("cars.cars"))

    if users_match(car.owner_id, current_user):
        flash("You cannot book your own car")
        return redirect(url_for("cars.car_detail", car_id=car_id))

    success, message = create_booking(car_id, current_user, start_date, end_date)

    flash(message)

    if success:
        return redirect(url_for("cars.bookings"))

    return redirect(url_for("cars.car_detail", car_id=car_id))


@cars_bp.route("/bookings")
def bookings():
    current_user = get_current_user()

    if current_user is None:
        flash("You must be logged in first")
        return redirect(url_for("auth.login"))

    my_bookings = Booking.get_bookings_by_renter(current_user)

    booking_details = []

    for booking in my_bookings:
        car = Car.get_car_by_id(booking.car_id)

        booking_details.append({
            "booking": booking,
            "car": car
        })

    return render_template("cars/my_bookings.html", bookings=booking_details)