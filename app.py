"""
Main application file to create and configure the application.
"""

from flask import Flask
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.tutor_routes import tutor_bp
from routes.admin_routes import admin_bp
from services.rate_limiting import limiter
from config import Config
from repositories.data_store import initialize_data


def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    # Initialize data store
    initialize_data()

    # Initialize rate limiting
    limiter.init_app(flask_app)

    # Register Blueprints
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(student_bp)
    flask_app.register_blueprint(tutor_bp)
    flask_app.register_blueprint(admin_bp)

    return flask_app


app = create_app()
