from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "development-secret-key"

    @app.route("/")
    def home():
        return "Lab Equipments Booking System"

    return app