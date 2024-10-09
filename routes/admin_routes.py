"""
Routes for administrators.
"""

from flask import Blueprint, jsonify, g
from services.authorization import admin_required
from repositories.user_repository import UserRepository

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/dashboard", methods=["GET"])
@admin_required
def admin_dashboard():
    """
    Endpoint for administrators to view their dashboard.
    """
    admin = UserRepository.get_user_by_id(g.user_id)
    return (
        jsonify(
            {
                "message": f"Welcome to the admin dashboard, {admin.name}",
                "users": [user.email for user in UserRepository.users.values()],
            }
        ),
        200,
    )
