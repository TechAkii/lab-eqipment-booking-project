
"""
Tests for booking validation in the Lab Equipment Booking System.

These tests cover invalid booking details, equipment availability,
booking duration, past dates, and overlapping bookings.
"""

from datetime import datetime, time, timedelta

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Booking, Equipment, User


def local_today():
    """Return today's date in the system's local timezone."""
    return datetime.now().astimezone().date()


def create_student_and_equipment(client):
    """Create a Student and available equipment for a booking test."""

    with client.application.app_context():
        # Create a test Student account.
        student = User(
            username="booking_test_student",
            email="booking_test_student@example.com",
            password_hash=generate_password_hash("TestPassword123"),
            role="Student",
        )
        db.session.add(student)

        # Create equipment that can be booked.
        equipment = Equipment(
            name="Booking Test Microscope",
            category="Laboratory",
            description="Equipment created for automated tests",
            status="Available",
        )
        db.session.add(equipment)
        db.session.commit()

        student_id = student.id
        equipment_id = equipment.id

    # Log in the Student through the Flask-Login test session.
    with client.session_transaction() as session:
        session["_user_id"] = str(student_id)
        session["_fresh"] = True

    return equipment_id


def submit_booking(
    client,
    equipment_id,
    booking_date,
    start_time,
    end_time,
):
    """Submit a booking request using the application's actual form fields."""

    return client.post(
        "/booking/new",
        data={
            "equipment_id": str(equipment_id),
            "booking_date": booking_date.isoformat(),
            "start_time": start_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M"),
        },
        follow_redirects=True,
    )


def test_booking_rejects_missing_required_fields(client):
    """Reject a booking when required form fields are missing."""

    create_student_and_equipment(client)

    response = client.post(
        "/booking/new",
        data={},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"valid equipment, date, and times" in response.data.lower()


def test_booking_rejects_invalid_date(client):
    """Reject a booking with an invalid date or time value."""

    equipment_id = create_student_and_equipment(client)

    response = client.post(
        "/booking/new",
        data={
            "equipment_id": str(equipment_id),
            "booking_date": "not-a-date",
            "start_time": "10:00",
            "end_time": "11:00",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"valid equipment, date, and times" in response.data.lower()


def test_booking_rejects_end_before_start(client):
    """Reject a booking when its end time is before its start time."""

    equipment_id = create_student_and_equipment(client)
    booking_date = local_today() + timedelta(days=2)

    response = submit_booking(
        client,
        equipment_id,
        booking_date,
        time(11, 0),
        time(10, 0),
    )

    assert response.status_code == 200
    assert b"end time must be after" in response.data.lower()


def test_booking_rejects_past_date(client):
    """Reject a booking for a date in the past."""

    equipment_id = create_student_and_equipment(client)
    booking_date = local_today() - timedelta(days=2)

    response = submit_booking(
        client,
        equipment_id,
        booking_date,
        time(10, 0),
        time(11, 0),
    )

    assert response.status_code == 200
    assert b"cannot book a date in the past" in response.data.lower()


def test_booking_rejects_unavailable_equipment(client):
    """Reject a booking when the equipment is unavailable."""

    equipment_id = create_student_and_equipment(client)

    with client.application.app_context():
        equipment = db.session.get(Equipment, equipment_id)
        equipment.status = "Unavailable"
        db.session.commit()

    response = submit_booking(
        client,
        equipment_id,
        local_today() + timedelta(days=2),
        time(10, 0),
        time(11, 0),
    )

    assert response.status_code == 200
    assert b"not available for booking" in response.data.lower()


def test_booking_rejects_duration_under_30_minutes(client):
    """Reject a booking shorter than 30 minutes."""

    equipment_id = create_student_and_equipment(client)

    response = submit_booking(
        client,
        equipment_id,
        local_today() + timedelta(days=2),
        time(10, 0),
        time(10, 20),
    )

    assert response.status_code == 200
    assert b"between 30 minutes and 4 hours" in response.data.lower()


def test_booking_rejects_duration_over_4_hours(client):
    """Reject a booking longer than four hours."""

    equipment_id = create_student_and_equipment(client)

    response = submit_booking(
        client,
        equipment_id,
        local_today() + timedelta(days=2),
        time(9, 0),
        time(13, 30),
    )

    assert response.status_code == 200
    assert b"between 30 minutes and 4 hours" in response.data.lower()


def test_booking_rejects_overlapping_booking(client):
    """Reject a booking that overlaps an existing Pending booking."""

    equipment_id = create_student_and_equipment(client)
    booking_date = local_today() + timedelta(days=2)

    with client.application.app_context():
        student = User.query.filter_by(
            username="booking_test_student"
        ).first()

        existing_booking = Booking(
            user_id=student.id,
            equipment_id=equipment_id,
            booking_date=booking_date,
            start_time=time(10, 0),
            end_time=time(11, 0),
            status="Pending",
        )
        db.session.add(existing_booking)
        db.session.commit()

    response = submit_booking(
        client,
        equipment_id,
        booking_date,
        time(10, 30),
        time(11, 30),
    )

    assert response.status_code == 200
    assert b"already has a booking" in response.data.lower()
