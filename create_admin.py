
from getpass import getpass

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    print("Create the initial Admin account")

    if User.query.filter_by(role="Admin").first():
        print("An Admin account already exists. No account created.")
    else:
        username = input("Admin username: ").strip()
        email = input("Admin email: ").strip().lower()
        password = getpass("Admin password (minimum 8 characters): ")
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
            admin = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role="Admin",
            )

            db.session.add(admin)
            db.session.commit()

            print("Admin account created successfully.")
