import pytest
from app import app
from services.authentication import hash_password
from repositories.user_repository import UserRepository
import jwt
from config import Config


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_student_access(client):
    """
    Test that a student can access student dashboard.
    """
    token = jwt.encode(
        {
            "id": "1",
            "role": "student",
            "name": "John",
            "email": "student@example.com",
        },
        Config.JWT_SECRET_KEY,
        algorithm="HS256",
    )
    response = client.get(
        "/student/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_tutor_access_denied_to_student_route(client):
    """
    Test that a tutor cannot access student dashboard.
    """
    token = jwt.encode(
        {"user_id": "2", "role": "tutor"}, Config.JWT_SECRET_KEY, algorithm="HS256"
    )
    response = client.get(
        "/student/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.get_json()["message"] == "Access forbidden: Students only"
