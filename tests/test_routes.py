import pytest
from app import app
from repositories.data_store import initialize_data
from services.authentication import hash_password
from repositories.user_repository import UserRepository
import jwt
from config import Config


@pytest.fixture
def client():
    initialize_data()
    with app.test_client() as client:
        yield client


def test_get_student_dashboard(client):
    """
    Test accessing the student dashboard.
    """
    token = jwt.encode(
        {"user_id": "1", "role": "student"}, Config.JWT_SECRET_KEY, algorithm="HS256"
    )
    response = client.get(
        "/student/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Welcome to your dashboard" in response.get_json()["message"]


def test_get_tutor_dashboard(client):
    """
    Test accessing the tutor dashboard.
    """
    token = jwt.encode(
        {"user_id": "2", "role": "tutor"}, Config.JWT_SECRET_KEY, algorithm="HS256"
    )
    response = client.get(
        "/tutor/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Welcome to your dashboard" in response.get_json()["message"]


def test_student_enroll_in_class(client):
    """
    Test a student enrolling in a class.
    """
    token = jwt.encode(
        {"user_id": "1", "role": "student"}, Config.JWT_SECRET_KEY, algorithm="HS256"
    )
    response = client.post(
        "/student/enroll",
        headers={"Authorization": f"Bearer {token}"},
        json={"class_id": "101"},
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Enrolled successfully"
