
from getpass import getpass

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    print("Create the initial Staff account")

    if User.query.filter_by(role="Staff").first():
        print("An Staff account already exists. No account created.")
    else:
        username = input("Staff username: ").strip()
        email = input("Staff email: ").strip().lower()
        password = getpass("Staff password (minimum 8 characters): ")
        confirm_password = getpass("Confirm password: ")

        if not username or not email or not password:
            print("Error: All fields are required.")

        elif len(password) < 8:
            print("Error: Password must contain at least 8 characters.")

        elif password != confirm_password:
            print("Error: Passwords do not match.")

        elif (
            User.query.filter_by(username=username).first()
            or User.query.filter_by(email=email).first()
        ):
            print("Error: Username or email is already registered.")

        else:
            staff = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role="Staff",
            )

            db.session.add(staff)
            db.session.commit()

            print("Staff account created successfully.")
