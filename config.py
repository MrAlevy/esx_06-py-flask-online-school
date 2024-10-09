"""
Configuration class for the Flask application.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class Config:
    """
    Configuration class for the Flask application.
    """

    # pylint: disable=too-few-public-methods # Public methods are not needed in this class
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SECURITY_ENABLED = os.getenv("SECURITY_ENABLED", "True") == "True"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
