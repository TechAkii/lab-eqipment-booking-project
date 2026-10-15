
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

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return render_template("auth/register.html")

        existing_user = User.query.filter(
            or_(
                User.username == username,
                User.email == email,
            )
        ).first()

        if existing_user:
            flash(
                "Username or email is already registered.",
                "danger",
            )
            return render_template("auth/register.html")

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role="Student",
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email.lower(),
            )
        ).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            next_page = request.form.get("next", "").strip()

            # Allow only local application paths.
            if next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            return redirect(url_for("catalogue"))

        flash("Invalid username/email or password.", "danger")

    return render_template("auth/login.html")


@auth.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
