from flask import Flask

from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "development-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lab_equipment.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app import models

        db.create_all()

    @app.route("/")
    def home():
        return "Lab Equipment Booking System"

    return app