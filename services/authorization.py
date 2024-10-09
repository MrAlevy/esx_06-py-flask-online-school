"""
This module contains decorators to ensure that the user has the required role.
"""

from functools import wraps
from flask import request, jsonify, g
import jwt
from config import Config


def token_required(f):
    """
    Decorator to ensure the user provides a valid JWT token.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Decorator to ensure the user provides a valid JWT token.
        """
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            g.user_id = data["user_id"]
            g.role = data["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 401
        return f(*args, **kwargs)

    return decorated


def role_required(required_role):
    """
    Decorator factory to create role-based decorators.
    """

    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            """
            Decorator to ensure the user has the required role.
            """
            if g.role != required_role:
                return (
                    jsonify(
                        {
                            "message": f"Access forbidden: {required_role.capitalize()}s only"
                        }
                    ),
                    403,
                )
            return f(*args, **kwargs)

        return decorated

    return decorator


def student_required(f):
    """
    RBAC user is a student.
    """
    return role_required("student")(f)


def tutor_required(f):
    """
    RBAC user is a tutor.
    """
    return role_required("tutor")(f)


def admin_required(f):
    """
    RBAC user is an admin.
    """
    return role_required("admin")(f)
