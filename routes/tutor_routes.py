"""
Routes for tutor role.
"""

import uuid
from flask import Blueprint, request, jsonify, g
from services.authorization import tutor_required
from services.event_monitoring import log_event
from repositories.class_repository import ClassRepository
from repositories.user_repository import UserRepository
from models.class_model import Class

tutor_bp = Blueprint("tutor", __name__)


@tutor_bp.route("/tutor/dashboard", methods=["GET"])
@tutor_required
def tutor_dashboard():
    """
    Endpoint for tutors to view their dashboard.
    """
    tutor = UserRepository.get_user_by_id(g.user_id)
    teaching_classes = []
    for class_id in tutor.teaching_classes:
        class_obj = ClassRepository.get_class_by_id(class_id)
        if class_obj:
            teaching_classes.append({"id": class_obj.id, "name": class_obj.name})
    return (
        jsonify(
            {
                "message": f"Welcome to your dashboard, {tutor.name}",
                "teaching_classes": teaching_classes,
            }
        ),
        200,
    )


@tutor_bp.route("/tutor/classes", methods=["POST"])
@tutor_required
def create_class():
    """
    Endpoint for a tutor to create a new class.
    """
    data = request.get_json()
    class_name = data.get("name")
    if not class_name:
        return jsonify({"message": "Class name is required"}), 400

    # Create new class
    class_id = str(uuid.uuid4())
    new_class = Class(class_id, class_name, g.user_id)
    ClassRepository.create_class(new_class)

    # Add class to tutor's teaching classes
    tutor = UserRepository.get_user_by_id(g.user_id)
    tutor.teaching_classes.append(class_id)
    log_event(f"Tutor {tutor.email} created class {class_name}")
    return jsonify({"message": "Class created successfully", "class_id": class_id}), 201


@tutor_bp.route("/tutor/classes/<class_id>", methods=["PUT"])
@tutor_required
def update_class(class_id):
    """
    Endpoint for a tutor to update a class they teach.
    """
    data = request.get_json()
    class_obj = ClassRepository.get_class_by_id(class_id)
    if not class_obj:
        return jsonify({"message": "Class not found"}), 404

    if class_obj.tutor_id != g.user_id:
        return jsonify({"message": "Unauthorized to update this class"}), 403

    # Update class details
    class_obj.name = data.get("name", class_obj.name)
    ClassRepository.update_class(class_id, class_obj)
    log_event(f"Tutor {g.user_id} updated class {class_id}")
    return jsonify({"message": "Class updated successfully"}), 200


@tutor_bp.route("/tutor/classes/<class_id>", methods=["DELETE"])
@tutor_required
def delete_class(class_id):
    """
    Endpoint for a tutor to delete a class they teach.
    """
    class_obj = ClassRepository.get_class_by_id(class_id)
    if not class_obj:
        return jsonify({"message": "Class not found"}), 404

    if class_obj.tutor_id != g.user_id:
        return jsonify({"message": "Unauthorized to delete this class"}), 403

    # Delete class
    ClassRepository.delete_class(class_id)
    tutor = UserRepository.get_user_by_id(g.user_id)
    tutor.teaching_classes.remove(class_id)
    log_event(f"Tutor {g.user_id} deleted class {class_id}")
    return jsonify({"message": "Class deleted successfully"}), 200
