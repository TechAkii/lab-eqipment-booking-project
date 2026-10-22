from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_user, logout_user
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import User

# Creates a Blueprint to organize authentication-related routes.
auth = Blueprint("auth", __name__)


# Handles student registration and displays the registration page.
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Retrieves and cleans the submitted registration form values.
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Checks that all required registration fields are provided.
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        # Checks whether the password and confirmation match.
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        # Ensures the password meets the minimum length requirement.
        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return render_template("auth/register.html")

        # Checks whether the username or email is already registered.
        existing_user = User.query.filter(
            or_(
                User.username == username,
                User.email == email,
            )
        ).first()

        # Prevents registration with an existing username or email.
        if existing_user:
            flash(
                "Username or email is already registered.",
                "danger",
            )
            return render_template("auth/register.html")

        # Creates a new student account and securely hashes the password.
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role="Student",
        )

        # Adds the new user to the database and saves the changes.
        db.session.add(user)
        db.session.commit()

        # Confirms successful registration and redirects to the login page.
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    # Displays the registration form for GET requests.
    return render_template("auth/register.html")


# Handles user login and verifies the submitted credentials.
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Retrieves the username or email and password from the login form.
        username_or_email = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Finds a user by username or email.
        user = User.query.filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email.lower(),
            )
        ).first()

        # Verifies the password and logs in the user if the credentials are valid.
        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            # Retrieves the requested destination after login, if provided.
            next_page = request.form.get("next", "").strip()

            # Allows only local application paths to prevent external redirects.
            if next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            # Redirects to the catalogue when no valid destination is provided.
            return redirect(url_for("catalogue"))

        # Displays an error message when the login credentials are invalid.
        flash("Invalid username/email or password.", "danger")

    # Displays the login form for GET requests or unsuccessful login attempts.
    return render_template("auth/login.html")


# Logs out the currently authenticated user.
@auth.route("/logout", methods=["POST"])
def logout():
    # Ends the current user's login session.
    logout_user()

    # Confirms logout and redirects the user to the login page.
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
