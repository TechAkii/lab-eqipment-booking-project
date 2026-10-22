
from datetime import date, datetime, time

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager
from app.models import Booking, User
from app.permissions import role_required


# Creates the Flask application and configures its components, routes, and database.
def create_app(test_config=None):
    # Initializes the Flask application.
    app = Flask(__name__)

    # Configures the application secret key and database settings.
    app.config["SECRET_KEY"] = "development-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lab_equipment.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Applies custom configuration when provided, such as during testing.
    if test_config:
        app.config.update(test_config)

    # Initializes the database and login manager for this application.
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Imports the equipment model and authentication Blueprint.
    from app.models import Equipment
    from app.routes.auth import auth

    # Loads the logged-in user from the database using the user ID stored in the session.
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # -------------------- ADMIN LOGIN --------------------

    # Handles administrator login and redirects authenticated administrators to their dashboard.
    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if current_user.is_authenticated:
            if current_user.role == "Admin":
                return redirect(url_for("admin_dashboard"))
            logout_user()

        if request.method == "POST":
            # Retrieves the submitted username or email and password.
            username_or_email = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            # Finds the user by username or email.
            user = User.query.filter(
                db.or_(
                    User.username == username_or_email,
                    User.email == username_or_email.lower(),
                )
            ).first()

            # Verifies that the user exists, has the Admin role, and entered the correct password.
            if (
                user
                and user.role == "Admin"
                and check_password_hash(user.password_hash, password)
            ):
                login_user(user)
                flash("Admin login successful.", "success")
                return redirect(url_for("admin_dashboard"))

            # Displays an error message when the administrator credentials are invalid.
            flash("Invalid administrator credentials.", "danger")

        # Displays the administrator login page.
        return render_template("admin/login.html")

    # -------------------- ADMIN DASHBOARD --------------------

    # Displays the administrator dashboard with user, equipment, and booking totals.
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

    # Displays all users ordered by username for administrator management.
    @app.route("/admin/users")
    @role_required("Admin")
    def admin_users():
        users = User.query.order_by(User.username).all()

        return render_template(
            "admin/users.html",
            users=users,
        )

    # Creates a new Staff or Admin account after validating the submitted details.
    @app.route("/admin/users/create", methods=["POST"])
    @role_required("Admin")
    def admin_create_user():
        # Retrieves and cleans the submitted account details.
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        # Checks that all required account fields have been provided.
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("admin_users"))

        # Prevents usernames and email addresses from exceeding their length limits.
        if len(username) > 80 or len(email) > 120:
            flash("Username or email is too long.", "danger")
            return redirect(url_for("admin_users"))

        # Restricts account creation to Staff and Admin roles.
        if role not in {"Staff", "Admin"}:
            flash(
                "Only Staff and Admin accounts can be created here.",
                "danger",
            )
            return redirect(url_for("admin_users"))

        # Ensures the password meets the minimum length requirement.
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("admin_users"))

        # Checks whether the username or email is already registered.
        existing_user = User.query.filter(
            db.or_(
                User.username == username,
                User.email == email,
            )
        ).first()

        # Prevents the creation of duplicate accounts.
        if existing_user:
            flash("Username or email already exists.", "danger")
            return redirect(url_for("admin_users"))

        # Creates the account and stores a hashed password.
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
        )

        # Saves the new account to the database.
        db.session.add(user)
        db.session.commit()

        # Confirms account creation and returns to the user management page.
        flash(f"{role} account created successfully.", "success")
        return redirect(url_for("admin_users"))

    # Removes an eligible user account while protecting administrator access and booking history.
    @app.route(
        "/admin/users/<int:user_id>/delete",
        methods=["POST"],
    )
    @role_required("Admin")
    def admin_delete_user(user_id):
        # Retrieves the user account using its database ID.
        user = db.session.get(User, user_id)

        # Handles attempts to delete a user who does not exist.
        if user is None:
            flash("User not found.", "danger")
            return redirect(url_for("admin_users"))

        # Prevents an administrator from deleting their own account.
        if user.id == current_user.id:
            flash("You cannot remove your own Admin account.", "danger")
            return redirect(url_for("admin_users"))

        # Allows deletion only for Student and Staff accounts.
        if user.role not in {"Student", "Staff"}:
            flash(
                "Only Student and Staff accounts can be removed here.",
                "danger",
            )
            return redirect(url_for("admin_users"))

        # Preserves booking history by preventing deletion of users with bookings.
        if user.bookings:
            flash(
                "This account has booking history and cannot be deleted.",
                "warning",
            )
            return redirect(url_for("admin_users"))

        # Deletes the eligible account and saves the database changes.
        db.session.delete(user)
        db.session.commit()

        # Confirms account deletion and returns to user management.
        flash("User account removed successfully.", "success")
        return redirect(url_for("admin_users"))

    # -------------------- STAFF LOGIN --------------------

    # Handles staff login and redirects authenticated staff to booking approvals.
    @app.route("/staff/login", methods=["GET", "POST"])
    def staff_login():
        if current_user.is_authenticated:
            if current_user.role == "Staff":
                return redirect(url_for("staff_approvals"))
            logout_user()

        if request.method == "POST":
            # Retrieves the submitted username or email and password.
            username_or_email = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            # Finds the user by username or email.
            user = User.query.filter(
                db.or_(
                    User.username == username_or_email,
                    User.email == username_or_email.lower(),
                )
            ).first()

            # Verifies that the user exists, has the Staff role, and entered the correct password.
            if (
                user
                and user.role == "Staff"
                and check_password_hash(user.password_hash, password)
            ):
                login_user(user)
                flash("Staff login successful.", "success")
                return redirect(url_for("staff_approvals"))

            # Displays an error message when the staff credentials are invalid.
            flash("Invalid staff credentials.", "danger")

        # Displays the staff login page.
        return render_template("staff/login.html")

    # -------------------- DATABASE INITIALIZATION --------------------

    # Creates database tables and inserts the default equipment records.
    with app.app_context():
        db.create_all()

        # Imports and runs the equipment seeding function.
        from app.seed import seed_equipment

        seed_equipment()

    # Registers the authentication routes with the Flask application.
    app.register_blueprint(auth)

    # -------------------- EQUIPMENT CATALOGUE --------------------

    # Displays the home page with all equipment and available categories.
    @app.route("/")
    def home():
        # Retrieves equipment ordered alphabetically by name.
        equipment_items = Equipment.query.order_by(Equipment.name).all()

        # Retrieves the distinct equipment categories in alphabetical order.
        categories = [
            category
            for (category,) in (
                db.session.query(Equipment.category)
                .distinct()
                .order_by(Equipment.category)
                .all()
            )
        ]

        # Sends equipment and categories to the catalogue template.
        return render_template(
            "main/catalogue.html",
            equipment_items=equipment_items,
            categories=categories,
        )

    # Displays the equipment catalogue with optional search and category filters.
    @app.route("/catalogue")
    def catalogue():
        # Retrieves the search term and selected category from the URL parameters.
        search_query = request.args.get("q", "").strip()
        selected_category = request.args.get("category", "").strip()

        # Starts a query for all equipment records.
        query = Equipment.query

        # Filters equipment by name or description when a search term is provided.
        if search_query:
            query = query.filter(
                db.or_(
                    Equipment.name.ilike(f"%{search_query}%"),
                    Equipment.description.ilike(f"%{search_query}%"),
                )
            )

        # Filters equipment by the selected category when provided.
        if selected_category:
            query = query.filter(Equipment.category == selected_category)

        # Retrieves the filtered equipment ordered alphabetically by name.
        equipment_items = query.order_by(Equipment.name).all()

        # Retrieves all distinct equipment categories for the filter controls.
        categories = [
            category
            for (category,) in (
                db.session.query(Equipment.category)
                .distinct()
                .order_by(Equipment.category)
                .all()
            )
        ]

        # Displays the filtered equipment and available categories.
        return render_template(
            "main/catalogue.html",
            equipment_items=equipment_items,
            categories=categories,
        )

    # -------------------- STUDENT BOOKING --------------------

    # Allows logged-in students to submit equipment booking requests.
    @app.route("/booking/new", methods=["GET", "POST"])
    @login_required
    def new_booking():
        # Restricts booking requests to Student accounts.
        if current_user.role != "Student":
            flash(
                "Only students can request equipment bookings.",
                "danger",
            )
            return redirect(url_for("catalogue"))

        # Retrieves available equipment options and today's date.
        equipment_items = Equipment.query.order_by(Equipment.name).all()
        today = datetime.now().astimezone().date()

        if request.method == "POST":
            # Converts submitted equipment, date, and time values into the required data types.
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
            # Handles invalid or missing equipment, date, and time values.
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

            # Retrieves the selected equipment record from the database.
            equipment = db.session.get(Equipment, equipment_id)

            # Validates equipment availability, booking date, and time order.
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
                # Calculates the booking duration in minutes.
                start_minutes = start_time.hour * 60 + start_time.minute
                end_minutes = end_time.hour * 60 + end_time.minute
                duration = end_minutes - start_minutes

                # Retrieves the current local date and time.
                now = datetime.now().astimezone()
                current_time = now.time().replace(
                    second=0,
                    microsecond=0,
                )

                # Ensures bookings last at least 30 minutes and no more than 4 hours.
                if duration < 30 or duration > 240:
                    flash(
                        "Bookings must last between 30 minutes and 4 hours.",
                        "danger",
                    )
                # Prevents students from selecting a start time that has already passed today.
                elif (
                    booking_date == today
                    and start_time <= current_time
                ):
                    flash(
                        "The booking start time must be in the future.",
                        "danger",
                    )
                else:
                    # Checks for overlapping Pending or Approved bookings for the same equipment.
                    overlapping_booking = Booking.query.filter(
                        Booking.equipment_id == equipment.id,
                        Booking.booking_date == booking_date,
                        Booking.status.in_(["Pending", "Approved"]),
                        Booking.start_time < end_time,
                        Booking.end_time > start_time,
                    ).first()

                    # Prevents a new booking when another active booking overlaps the requested time.
                    if overlapping_booking:
                        flash(
                            "This equipment already has a booking "
                            "during that time.",
                            "danger",
                        )
                    else:
                        # Creates a new booking request with Pending status.
                        booking = Booking(
                            user_id=current_user.id,
                            equipment_id=equipment.id,
                            booking_date=booking_date,
                            start_time=start_time,
                            end_time=end_time,
                            status="Pending",
                        )

                        # Saves the booking request to the database.
                        db.session.add(booking)
                        db.session.commit()

                        # Confirms submission and redirects to the student's bookings page.
                        flash(
                            "Booking request submitted successfully.",
                            "success",
                        )
                        return redirect(url_for("my_bookings"))

            # Re-displays the booking form with equipment options after validation errors.
            return render_template(
                "main/new_booking.html",
                equipment_items=equipment_items,
                today=today.isoformat(),
            )

        # Displays the booking form for GET requests.
        return render_template(
            "main/new_booking.html",
            equipment_items=equipment_items,
            today=today.isoformat(),
        )

    # -------------------- MY BOOKINGS --------------------

    # Displays the booking history belonging to the currently logged-in student.
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

        # Retrieves the current local time for the booking history template.
        now = datetime.now().astimezone()
        current_time = now.time().replace(
            tzinfo=None,
            second=0,
            microsecond=0,
        )

        # Sends the student's bookings and current date/time to the template.
        return render_template(
            "main/my_bookings.html",
            bookings=bookings,
            today=now.date(),
            current_time=current_time,
        )

    # -------------------- STAFF APPROVALS --------------------

    # -------------------- STAFF APPROVALS --------------------

    # Displays all bookings so staff can review their statuses and booking details.
    @app.route("/staff/approvals")
    @role_required("Staff")
    def staff_approvals():
        # Retrieves all bookings, ordered by most recent date and start time.
        bookings = (
            Booking.query
            .order_by(
                Booking.booking_date.desc(),
                Booking.start_time.desc(),
            )
            .all()
        )

        # Sends the booking records to the staff approvals page.
        return render_template(
            "staff/approvals.html",
            bookings=bookings,
        )

    # Approves a booking only if it exists and is still Pending.
    @app.route(
        "/staff/approvals/<int:booking_id>/approve",
        methods=["POST"],
    )
    @role_required("Staff")
    def approve_booking(booking_id):
        # Retrieves the selected booking using its database ID.
        booking = db.session.get(Booking, booking_id)

        # Handles missing bookings and bookings that have already been reviewed.
        if booking is None:
            flash("Booking not found.", "danger")
        elif booking.status != "Pending":
            flash("This booking has already been reviewed.", "warning")
        else:
            # Changes the booking status to Approved and saves the change.
            booking.status = "Approved"
            db.session.commit()
            flash("Booking approved successfully.", "success")

        # Returns to the staff approvals page after processing the request.
        return redirect(url_for("staff_approvals"))

    # Rejects a booking only if it exists, is Pending, and has a rejection reason.
    @app.route(
        "/staff/approvals/<int:booking_id>/reject",
        methods=["POST"],
    )
    @role_required("Staff")
    def reject_booking(booking_id):
        # Retrieves the selected booking using its database ID.
        booking = db.session.get(Booking, booking_id)

        # Handles missing bookings and bookings that have already been reviewed.
        if booking is None:
            flash("Booking not found.", "danger")
        elif booking.status != "Pending":
            flash("This booking has already been reviewed.", "warning")
        else:
            # Retrieves and cleans the rejection reason submitted by staff.
            reason = request.form.get("rejection_reason", "").strip()

            # Requires a reason before a booking can be rejected.
            if not reason:
                flash(
                    "Please provide a reason for rejection.",
                    "danger",
                )
                return redirect(url_for("staff_approvals"))

            # Updates the booking status and stores the rejection reason.
            booking.status = "Rejected"
            booking.rejection_reason = reason
            db.session.commit()
            flash("Booking rejected successfully.", "success")

        # Returns to the staff approvals page after processing the request.
        return redirect(url_for("staff_approvals"))

    # Returns the configured Flask application instance.
    return app