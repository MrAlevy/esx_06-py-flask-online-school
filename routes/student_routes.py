"""
Routes for student role.
"""

from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from services.authorization import student_required
from services.event_monitoring import log_event
from services.encryption import EncryptionService
from repositories.user_repository import UserRepository
from repositories.class_repository import ClassRepository
from utils.validators import UpdateStudentModel


student_bp = Blueprint("student", __name__)
encryption_service = EncryptionService()


@student_bp.route("/student/dashboard", methods=["GET"])
@student_required
def student_dashboard():
    """
    Endpoint for students to view their dashboard.
    """
    student = UserRepository.get_user_by_id(g.user_id)
    enrolled_classes = []
    for class_id in student.enrolled_classes:
        class_obj = ClassRepository.get_class_by_id(class_id)
        if class_obj:
            enrolled_classes.append({"id": class_obj.id, "name": class_obj.name})
    return (
        jsonify(
            {
                "message": f"Welcome to your dashboard, {student.name}",
                "enrolled_classes": enrolled_classes,
                "grades": student.grades,
                "ssn": encryption_service.decrypt(student.ssn_encrypted),
            }
        ),
        200,
    )


@student_bp.route("/student/classes", methods=["GET"])
@student_required
def get_available_classes():
    """
    Endpoint to get a list of all available classes.
    """
    classes = ClassRepository.get_all_classes()
    class_list = [{"id": c.id, "name": c.name} for c in classes]
    return jsonify({"available_classes": class_list}), 200


@student_bp.route("/student/enroll", methods=["POST"])
@student_required
def enroll_in_class():
    """
    Endpoint for a student to enroll in a class.
    """
    data = request.get_json()
    class_id = data.get("class_id")
    class_obj = ClassRepository.get_class_by_id(class_id)
    if not class_obj:
        return jsonify({"message": "Class not found"}), 404

    student = UserRepository.get_user_by_id(g.user_id)
    if class_id in student.enrolled_classes:
        return jsonify({"message": "Already enrolled in this class"}), 400

    # Enroll student in class
    student.enrolled_classes.append(class_id)
    class_obj.student_ids.append(student.id)
    log_event(f"Student {student.email} enrolled in class {class_id}")
    return jsonify({"message": "Enrolled successfully"}), 200


@student_bp.route("/student/profile", methods=["PUT"])
@student_required
def update_student_profile():
    """
    Endpoint for a student to update their profile, including encrypted fields.
    """
    try:
        data = request.get_json()
        validated_data = UpdateStudentModel(**data)

        student = UserRepository.get_user_by_id(g.user_id)
        if not student:
            return jsonify({"message": "Student not found"}), 404

        # Update student's name
        if validated_data.name:
            student.name = validated_data.name

        # Update and encrypt SSN
        if validated_data.ssn:
            student.ssn_encrypted = encryption_service.encrypt(validated_data.ssn)

        log_event(f"Student {student.email} updated their profile")
        return jsonify({"message": "Profile updated successfully"}), 200
    except ValidationError as e:
        return jsonify({"message": "Invalid input", "errors": e.errors()}), 400
