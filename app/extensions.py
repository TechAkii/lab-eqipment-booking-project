
# Imports Flask-Login's manager for handling user authentication sessions.
from flask_login import LoginManager

# Imports Flask-SQLAlchemy for database integration and ORM operations.
from flask_sqlalchemy import SQLAlchemy

# Creates the database object used to interact with the application's database.
db = SQLAlchemy()

# Creates the login manager used to manage user login sessions.
login_manager = LoginManager()
