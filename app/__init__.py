
from datetime import date, datetime, time

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "development-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lab_equipment.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models import Booking, Equipment, User
    from app.routes.auth import auth

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth)

    @app.route("/")
    def home():
        return render_template(
            "main/catalogue.html",
            equipment_items=Equipment.query.order_by(Equipment.name).all(),
            categories=[
                category
                for (category,) in (
                    db.session.query(Equipment.category)
                    .distinct()
                    .order_by(Equipment.category)
                    .all()
                )
            ],
        )

    @app.route("/catalogue")
    def catalogue():
        search_query = request.args.get("q", "").strip()
        selected_category = request.args.get("category", "").strip()

        query = Equipment.query

        if search_query:
            query = query.filter(
                db.or_(
                    Equipment.name.ilike(f"%{search_query}%"),
                    Equipment.description.ilike(f"%{search_query}%"),
                )
            )

        if selected_category:
            query = query.filter(
                Equipment.category == selected_category
            )

        equipment_items = query.order_by(Equipment.name).all()

        categories = [
            category
            for (category,) in (
                db.session.query(Equipment.category)
                .distinct()
                .order_by(Equipment.category)
                .all()
            )
        ]

        return render_template(
            "main/catalogue.html",
            equipment_items=equipment_items,
            categories=categories,
        )

    @app.route("/booking/new", methods=["GET", "POST"])
    @login_required
    def new_booking():
        if current_user.role != "Student":
            flash(
                "Only students can request equipment bookings.",
                "danger",
            )
            return redirect(url_for("catalogue"))

        equipment_items = Equipment.query.order_by(Equipment.name).all()
        today = datetime.now().astimezone().date()

        if request.method == "POST":
            try:
                equipment_id = int(request.form.get("equipment_id", ""))
                booking_date = date.fromisoformat(
                    request.form.get("booking_date", "")
                )
                start_time = time.fromisoformat(
                    request.form.get("start_time", "")
                )
                end_time = time.fromisoformat(
                    request.form.get("end_time", "")
                )
            except (ValueError, TypeError):
                flash(
                    "Please enter valid equipment, date, and times.",
                    "danger",
                )
                return render_template(
                    "main/new_booking.html",
                    equipment_items=equipment_items,
                    today=today.isoformat(),
                )

            equipment = db.session.get(Equipment, equipment_id)

            if equipment is None or equipment.status != "Available":
                flash(
                    "That equipment is not available for booking.",
                    "danger",
                )
            elif booking_date < today:
                flash("You cannot book a date in the past.", "danger")
            elif end_time <= start_time:
                flash(
                    "The end time must be after the start time.",
                    "danger",
                )
            else:
                start_minutes = start_time.hour * 60 + start_time.minute
                end_minutes = end_time.hour * 60 + end_time.minute
                duration = end_minutes - start_minutes

                now = datetime.now().astimezone()
                current_time = now.time().replace(
                    second=0,
                    microsecond=0,
                )

                if duration < 30 or duration > 240:
                    flash(
                        "Bookings must last between 30 minutes and 4 hours.",
                        "danger",
                    )
                elif (
                    booking_date == today
                    and start_time <= current_time
                ):
                    flash(
                        "The booking start time must be in the future.",
                        "danger",
                    )
                else:
                    overlapping_booking = Booking.query.filter(
                        Booking.equipment_id == equipment.id,
                        Booking.booking_date == booking_date,
                        Booking.status.in_(["Pending", "Approved"]),
                        Booking.start_time < end_time,
                        Booking.end_time > start_time,
                    ).first()

                    if overlapping_booking:
                        flash(
                            "This equipment already has a booking "
                            "during that time.",
                            "danger",
                        )
                    else:
                        booking = Booking(
                            user_id=current_user.id,
                            equipment_id=equipment.id,
                            booking_date=booking_date,
                            start_time=start_time,
                            end_time=end_time,
                            status="Pending",
                        )

                        db.session.add(booking)
                        db.session.commit()

                        flash(
                            "Booking request submitted successfully.",
                            "success",
                        )
                        return redirect(url_for("my_bookings"))

            return render_template(
                "main/new_booking.html",
                equipment_items=equipment_items,
                today=today.isoformat(),
            )

        return render_template(
            "main/new_booking.html",
            equipment_items=equipment_items,
            today=today.isoformat(),
        )


    
    @app.route("/my-bookings")
    @login_required
    def my_bookings():
        bookings = (
            Booking.query.filter_by(user_id=current_user.id)
            .order_by(
                Booking.booking_date.desc(),
                Booking.start_time.desc(),
            )
            .all()
        )

        return render_template(
            "main/my_bookings.html",
            bookings=bookings,
        )
        
        
    @app.route("/staff/approvals")
    @login_required
    def staff_approvals():
        if current_user.role != "Staff":
            flash("Access denied. Staff members only.", "danger")
            return redirect(url_for("catalogue"))

        pending_bookings = (
            Booking.query.filter_by(status="Pending")
            .order_by(Booking.booking_date, Booking.start_time)
            .all()
        )

        return render_template(
            "staff/approvals.html",
            bookings=pending_bookings,
        )

    @app.route("/staff/approvals/<int:booking_id>/approve", methods=["POST"])
    @login_required
    def approve_booking(booking_id):
        if current_user.role != "Staff":
            flash("Access denied. Staff members only.", "danger")
            return redirect(url_for("catalogue"))

        booking = db.session.get(Booking, booking_id)

        if booking is None:
            flash("Booking not found.", "danger")
        elif booking.status != "Pending":
            flash("This booking has already been reviewed.", "warning")
        else:
            booking.status = "Approved"
            db.session.commit()
            flash("Booking approved successfully.", "success")

        return redirect(url_for("staff_approvals"))

    @app.route("/staff/approvals/<int:booking_id>/reject", methods=["POST"])
    @login_required
    def reject_booking(booking_id):
        if current_user.role != "Staff":
            flash("Access denied. Staff members only.", "danger")
            return redirect(url_for("catalogue"))

        booking = db.session.get(Booking, booking_id)

        if booking is None:
            flash("Booking not found.", "danger")
        elif booking.status != "Pending":
            flash("This booking has already been reviewed.", "warning")
        else:
            reason = request.form.get("rejection_reason", "").strip()

            if not reason:
                flash("Please provide a reason for rejection.", "danger")
                return redirect(url_for("staff_approvals"))

            booking.status = "Rejected"
            booking.rejection_reason = reason
            db.session.commit()
            flash("Booking rejected successfully.", "success")

        return redirect(url_for("staff_approvals"))



    return app
