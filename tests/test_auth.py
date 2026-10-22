
# Imports the User model to create and verify user records in the database.
from app.models import User


# Tests whether a student can register successfully with valid details.
def test_register_successfully(client, app):
    # Submits the registration form with valid user information.
    response = client.post(
        "/register",
        data={
            "username": "student1",
            "email": "student1@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        },
        follow_redirects=True,
    )

    # Checks that the registration request completes successfully.
    assert response.status_code == 200

    # Checks that a registration success message is displayed.
    assert b"Registration successful" in response.data

    # Creates an application context to query the database.
    with app.app_context():
        # Retrieves the newly registered user using their email address.
        user = User.query.filter_by(
            email="student1@example.com"
        ).first()

        # Verifies that the user was created with the Student role and a hashed password.
        assert user is not None
        assert user.role == "Student"
        assert user.password_hash != "StrongPass123"


# Tests whether registration is rejected when the passwords do not match.
def test_register_passwords_do_not_match(client):
    # Submits the registration form with different password values.
    response = client.post(
        "/register",
        data={
            "username": "student2",
            "email": "student2@example.com",
            "password": "StrongPass123",
            "confirm_password": "DifferentPass123",
        },
        follow_redirects=True,
    )

    # Checks that the registration page is returned successfully.
    assert response.status_code == 200

    # Checks that the password mismatch error message is displayed.
    assert b"Passwords do not match" in response.data


# Tests whether registration is rejected when the email already exists.
def test_register_duplicate_email(client, app):
    # Creates an existing user in the test database.
    with app.app_context():
        user = User(
            username="existing",
            email="existing@example.com",
            password_hash="test-hash",
            role="Student",
        )
        # Imports the database object for database operations.
        from app.extensions import db

        # Saves the existing user to the database.
        db.session.add(user)
        db.session.commit()

    # Attempts to register another user using the same email address.
    response = client.post(
        "/register",
        data={
            "username": "another",
            "email": "existing@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        },
        follow_redirects=True,
    )

    # Checks that the registration page is returned successfully.
    assert response.status_code == 200

    # Checks that the duplicate registration error message is displayed.
    assert b"already registered" in response.data


# Tests whether a user can log in with valid credentials.
def test_login_successfully(client, app):
    # Imports the password hashing function for creating a test user.
    from werkzeug.security import generate_password_hash

    # Imports the database object for database operations.
    from app.extensions import db

    # Creates a test user with a securely hashed password.
    with app.app_context():
        user = User(
            username="loginstudent",
            email="loginstudent@example.com",
            password_hash=generate_password_hash("StrongPass123"),
            role="Student",
        )
        # Saves the test user to the database.
        db.session.add(user)
        db.session.commit()

    # Submits the login form with valid credentials.
    response = client.post(
        "/login",
        data={
            "username": "loginstudent",
            "password": "StrongPass123",
        },
        follow_redirects=True,
    )

    # Checks that login and the subsequent page load succeed.
    assert response.status_code == 200

    # Checks that the equipment catalogue is displayed after login.
    assert b"Equipment Catalogue" in response.data


# Tests whether login is rejected when the password is incorrect.
def test_login_invalid_password(client, app):
    # Imports the password hashing function for creating a test user.
    from werkzeug.security import generate_password_hash

    # Imports the database object for database operations.
    from app.extensions import db

    # Creates a test user with a known password hash.
    with app.app_context():
        user = User(
            username="loginstudent",
            email="loginstudent@example.com",
            password_hash=generate_password_hash("StrongPass123"),
            role="Student",
        )
        # Saves the test user to the database.
        db.session.add(user)
        db.session.commit()

    # Attempts to log in using an incorrect password.
    response = client.post(
        "/login",
        data={
            "username": "loginstudent",
            "password": "WrongPassword123",
        },
        follow_redirects=True,
    )

    # Checks that the login page is returned successfully.
    assert response.status_code == 200

    # Checks that the invalid credentials error message is displayed.
    assert b"Invalid username/email or password" in response.data