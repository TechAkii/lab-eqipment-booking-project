
from datetime import date, datetime, time

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager
from app.models import User
from app.permissions import role_required


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "development-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lab_equipment.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models import Booking, Equipment
    from app.routes.auth import auth

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # -------------------- ADMIN LOGIN --------------------

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if current_user.is_authenticated:
            if current_user.role == "Admin":
                return redirect(url_for("admin_dashboard"))
            logout_user()

        if request.method == "POST":
            username_or_email = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            user = User.query.filter(
                db.or_(
                    User.username == username_or_email,
                    User.email == username_or_email.lower(),
                )
            ).first()

            if (
                user
                and user.role == "Admin"
                and check_password_hash(user.password_hash, password)
            ):
                login_user(user)
                flash("Admin login successful.", "success")
                return redirect(url_for("admin_dashboard"))

            flash("Invalid administrator credentials.", "danger")

        return render_template("admin/login.html")

    # -------------------- ADMIN DASHBOARD --------------------

    @app.route("/admin/dashboard")
    @role_required("Admin")
    def admin_dashboard():
        return render_template(
            "admin/dashboard.html",
            total_users=User.query.count(),
            total_students=User.query.filter_by(role="Student").count(),
            total_staff=User.query.filter_by(role="Staff").count(),
            total_admins=User.query.filter_by(role="Admin").count(),
            total_equipment=Equipment.query.count(),
            pending_bookings=Booking.query.filter_by(
                status="Pending"
            ).count(),
            approved_bookings=Booking.query.filter_by(
                status="Approved"
            ).count(),
            rejected_bookings=Booking.query.filter_by(
                status="Rejected"
            ).count(),
        )

    # -------------------- ADMIN USER MANAGEMENT --------------------

    @app.route("/admin/users")
    @role_required("Admin")
    def admin_users():
        users = User.query.order_by(User.username).all()

        return render_template(
            "admin/users.html",
            users=users,
        )

    @app.route("/admin/users/create", methods=["POST"])
    @role_required("Admin")
    def admin_create_user():
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("admin_users"))

        if len(username) > 80 or len(email) > 120:
            flash("Username or email is too long.", "danger")
            return redirect(url_for("admin_users"))

        if role not in {"Staff", "Admin"}:
            flash(
                "Only Staff and Admin accounts can be created here.",
                "danger",
            )
            return redirect(url_for("admin_users"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("admin_users"))

        existing_user = User.query.filter(
            db.or_(
                User.username == username,
                User.email == email,
            )
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("admin_users"))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
        )

        db.session.add(user)
        db.session.commit()

        flash(f"{role} account created successfully.", "success")
        return redirect(url_for("admin_users"))

    @app.route(
        "/admin/users/<int:user_id>/delete",
        methods=["POST"],
    )
    @role_required("Admin")
    def admin_delete_user(user_id):
        user = db.session.get(User, user_id)

        if user is None:
            flash("User not found.", "danger")
            return redirect(url_for("admin_users"))

        if user.id == current_user.id:
            flash("You cannot remove your own Admin account.", "danger")
            return redirect(url_for("admin_users"))

        if user.role not in {"Student", "Staff"}:
            flash(
                "Only Student and Staff accounts can be removed here.",
                "danger",
            )
            return redirect(url_for("admin_users"))

        # Preserve booking history.
        if user.bookings:
            flash(
                "This account has booking history and cannot be deleted.",
                "warning",
            )
            return redirect(url_for("admin_users"))

        db.session.delete(user)
        db.session.commit()

        flash("User account removed successfully.", "success")
        return redirect(url_for("admin_users"))

    # -------------------- STAFF LOGIN --------------------

    @app.route("/staff/login", methods=["GET", "POST"])
    def staff_login():
        if current_user.is_authenticated:
            if current_user.role == "Staff":
                return redirect(url_for("staff_approvals"))
            logout_user()

        if request.method == "POST":
            username_or_email = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            user = User.query.filter(
                db.or_(
                    User.username == username_or_email,
                    User.email == username_or_email.lower(),
                )
            ).first()

            if (
                user
                and user.role == "Staff"
                and check_password_hash(user.password_hash, password)
            ):
                login_user(user)
                flash("Staff login successful.", "success")
                return redirect(url_for("staff_approvals"))

            flash("Invalid staff credentials.", "danger")

        return render_template("staff/login.html")

    # -------------------- DATABASE INITIALIZATION --------------------

    with app.app_context():
        db.create_all()

        from app.seed import seed_equipment

        seed_equipment()

    app.register_blueprint(auth)

    # -------------------- EQUIPMENT CATALOGUE --------------------

    @app.route("/")
    def home():
        equipment_items = Equipment.query.order_by(Equipment.name).all()

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
            query = query.filter(Equipment.category == selected_category)

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

    # -------------------- STUDENT BOOKING --------------------

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

    # -------------------- MY BOOKINGS --------------------

    @app.route("/my-bookings")
    @login_required
    def my_bookings():
        # This page is intended for students. Staff and Admin users
        # must not access a student's personal booking history page.
        if current_user.role != "Student":
            flash("This page is for Student accounts only.", "danger")
            return redirect(url_for("catalogue"))

        # Return every booking for the logged-in student, including
        # Pending, Approved, Rejected, and bookings in the past.
        bookings = (
            Booking.query.filter_by(user_id=current_user.id)
            .order_by(
                Booking.booking_date.desc(),
                Booking.start_time.desc(),
            )
            .all()
        )

        now = datetime.now().astimezone()
        current_time = now.time().replace(
            tzinfo=None,
            second=0,
            microsecond=0,
        )

        return render_template(
            "main/my_bookings.html",
            bookings=bookings,
            today=now.date(),
            current_time=current_time,
        )

    # -------------------- STAFF APPROVALS --------------------

    @app.route("/staff/approvals")
    @role_required("Staff")
    def staff_approvals():
        pending_bookings = (
            Booking.query.filter_by(status="Pending")
            .order_by(Booking.booking_date, Booking.start_time)
            .all()
        )

        
        

        return render_template(
            "staff/approvals.html",
            bookings=pending_bookings,
        )

    @app.route(
        "/staff/approvals/<int:booking_id>/approve",
        methods=["POST"],
    )
    @role_required("Staff")
    def approve_booking(booking_id):
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

    @app.route(
        "/staff/approvals/<int:booking_id>/reject",
        methods=["POST"],
    )
    @role_required("Staff")
    def reject_booking(booking_id):
        booking = db.session.get(Booking, booking_id)

        if booking is None:
            flash("Booking not found.", "danger")
        elif booking.status != "Pending":
            flash("This booking has already been reviewed.", "warning")
        else:
            reason = request.form.get("rejection_reason", "").strip()

            if not reason:
                flash(
                    "Please provide a reason for rejection.",
                    "danger",
                )
                return redirect(url_for("staff_approvals"))

            booking.status = "Rejected"
            booking.rejection_reason = reason
            db.session.commit()
            flash("Booking rejected successfully.", "success")

        return redirect(url_for("staff_approvals"))

    return app
