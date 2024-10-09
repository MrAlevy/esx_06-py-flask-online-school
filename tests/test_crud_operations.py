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


def test_create_class(client):
    """
    Test that a tutor can create a class.
    """
    token = jwt.encode(
        {"user_id": "2", "role": "tutor"}, Config.JWT_SECRET_KEY, algorithm="HS256"
    )
    response = client.post(
        "/tutor/classes",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Advanced Python"},
    )
    assert response.status_code == 201
    assert "class_id" in response.get_json()


def test_enroll_in_class(client):
    """
    Test that a student can enroll in a class.
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
