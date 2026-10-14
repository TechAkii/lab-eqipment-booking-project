
from app.models import User


def test_register_successfully(client, app):
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

    assert response.status_code == 200
    assert b"Registration successful" in response.data

    with app.app_context():
        user = User.query.filter_by(
            email="student1@example.com"
        ).first()

        assert user is not None
        assert user.role == "Student"
        assert user.password_hash != "StrongPass123"


def test_register_passwords_do_not_match(client):
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

    assert response.status_code == 200
    assert b"Passwords do not match" in response.data


def test_register_duplicate_email(client, app):
    with app.app_context():
        user = User(
            username="existing",
            email="existing@example.com",
            password_hash="test-hash",
            role="Student",
        )
        from app.extensions import db

        db.session.add(user)
        db.session.commit()

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

    assert response.status_code == 200
    assert b"already registered" in response.data


def test_login_successfully(client, app):
    from app.extensions import db
    from werkzeug.security import generate_password_hash

    with app.app_context():
        user = User(
            username="loginstudent",
            email="loginstudent@example.com",
            password_hash=generate_password_hash("StrongPass123"),
            role="Student",
        )
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "username": "loginstudent",
            "password": "StrongPass123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Equipment Catalogue" in response.data


def test_login_invalid_password(client, app):
    from app.extensions import db
    from werkzeug.security import generate_password_hash

    with app.app_context():
        user = User(
            username="loginstudent",
            email="loginstudent@example.com",
            password_hash=generate_password_hash("StrongPass123"),
            role="Student",
        )
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "username": "loginstudent",
            "password": "WrongPassword123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid username/email or password" in response.data
