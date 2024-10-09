"""
Routes for user authentication.
"""

import uuid
import jwt
from pydantic import ValidationError

from flask import Blueprint, request, jsonify
from repositories.user_repository import UserRepository
from models.student import Student
from services.authentication import verify_password, hash_password
from services.rate_limiting import limiter
from services.event_monitoring import log_event
from utils.validators import LoginModel, SignupModel
from config import Config

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
@limiter.limit("5 per minute")
def signup():
    """
    Endpoint to register a new student user.
    """
    try:
        data = request.get_json()
        validated_data = SignupModel(**data)
        email = validated_data.email

        # Check if user already exists
        if UserRepository.get_user_by_email(email):
            return jsonify({"message": "User already exists"}), 400

        # Create new student user
        user_id = str(uuid.uuid4())
        password_hash = hash_password(validated_data.password)
        student = Student(user_id, validated_data.name, email, password_hash, "student")

        # Add user to repository
        UserRepository.add_user(student)
        log_event(f"New user registered: {email}")

        return jsonify({"message": "User registered successfully"}), 201
    except ValidationError as e:
        # Handle validation errors
        return jsonify({"message": "Invalid input", "errors": e.errors()}), 400


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """
    Endpoint to authenticate a user and provide a JWT token.
    """
    try:
        data = request.get_json()
        validated_data = LoginModel(**data)
        email = validated_data.email
        password = validated_data.password

        user = UserRepository.get_user_by_email(email)
        if user and verify_password(password, user.password_hash):
            # Generate JWT token
            token = jwt.encode(
                {"user_id": user.id, "role": user.role},
                Config.JWT_SECRET_KEY,
                algorithm="HS256",
            )
            log_event(f"User {email} logged in successfully.")
            return jsonify({"token": token}), 200

        log_event(f"Failed login attempt for email: {email}")
        return jsonify({"message": "Invalid credentials"}), 401
    except ValidationError as e:
        # Handle validation errors
        return jsonify({"message": "Invalid input", "errors": e.errors()}), 400
