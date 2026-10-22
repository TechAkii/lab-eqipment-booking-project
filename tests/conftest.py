
# Imports pytest for writing and running automated tests.
import pytest

# Imports the Flask application factory used to create the test application.
from app import create_app

# Imports the database object to create and clean up test database tables.
from app.extensions import db


# Creates a pytest fixture that provides a separate Flask application for testing.
@pytest.fixture
def app():
    # Creates the application with testing mode enabled and an in-memory SQLite database.
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
    })

    # Creates an application context so database operations can run during tests.
    with app.app_context():
        # Creates all database tables required by the application models.
        db.create_all()

        # Provides the configured application to tests that request this fixture.
        yield app

        # Removes the current database session after the test finishes.
        db.session.remove()

        # Deletes the test database tables to clean up after testing.
        db.drop_all()


# Creates a pytest fixture that provides a test client for sending requests to the application.
@pytest.fixture
def client(app):
    # Returns Flask's test client for testing routes without running a live server.
    return app.test_client()