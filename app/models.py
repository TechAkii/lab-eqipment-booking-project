
# Imports datetime to record when a booking was created.
from datetime import datetime

# Imports UserMixin to provide Flask-Login user session functionality.
from flask_login import UserMixin

# Imports the shared database object used by the application models.
from app.extensions import db


# Defines the User model for storing user account information.
class User(UserMixin, db.Model):
    # Sets the database table name for user accounts.
    __tablename__ = "users"

    # Defines the unique primary key for each user.
    id = db.Column(db.Integer, primary_key=True)

    # Stores the user's username, which must be unique and cannot be empty.
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Stores the user's email address, which must be unique and cannot be empty.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Stores the hashed password instead of the original password.
    password_hash = db.Column(db.String(255), nullable=False)

    # Stores the user's role, defaulting to Student when no role is provided.
    role = db.Column(db.String(20), nullable=False, default="Student")

    # Defines the relationship between a user and their bookings.
    bookings = db.relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# Defines the Equipment model for storing laboratory equipment details.
class Equipment(db.Model):
    # Sets the database table name for equipment records.
    __tablename__ = "equipment"

    # Defines the unique primary key for each equipment item.
    id = db.Column(db.Integer, primary_key=True)

    # Stores the name of the equipment.
    name = db.Column(db.String(120), nullable=False)

    # Stores the category to which the equipment belongs.
    category = db.Column(db.String(80), nullable=False)

    # Stores an optional description of the equipment.
    description = db.Column(db.Text, nullable=True)

    # Stores the equipment's availability status, defaulting to Available.
    status = db.Column(db.String(30), nullable=False, default="Available")

    # Defines the relationship between equipment and its bookings.
    bookings = db.relationship(
        "Booking",
        back_populates="equipment",
        cascade="all, delete-orphan",
    )


# Defines the Booking model for storing equipment reservation details.
class Booking(db.Model):
    # Sets the database table name for booking records.
    __tablename__ = "bookings"

    # Defines the unique primary key for each booking.
    id = db.Column(db.Integer, primary_key=True)

    # Stores the ID of the user who made the booking.
    # The foreign key links this value to the users table.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    # Stores the ID of the equipment being booked.
    # The foreign key links this value to the equipment table.
    equipment_id = db.Column(
        db.Integer,
        db.ForeignKey("equipment.id"),
        nullable=False,
    )

    # Stores the date on which the equipment is booked.
    booking_date = db.Column(db.Date, nullable=False)

    # Stores the starting time of the booking.
    start_time = db.Column(db.Time, nullable=False)

    # Stores the ending time of the booking.
    end_time = db.Column(db.Time, nullable=False)

    # Stores the booking status, defaulting to Pending.
    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending",
    )

    # Stores the reason for rejecting a booking, when applicable.
    rejection_reason = db.Column(db.Text, nullable=True)

    # Records the date and time when the booking record is created.
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    # Defines the relationship between a booking and its user.
    user = db.relationship(
        "User",
        back_populates="bookings",
    )

    # Defines the relationship between a booking and its equipment.
    equipment = db.relationship(
        "Equipment",
        back_populates="bookings",
    )