import pytest
from app import app
from repositories.data_store import initialize_data
from services.authentication import hash_password
from repositories.user_repository import UserRepository
import json


@pytest.fixture
def client():
    initialize_data()  # Ensure data is initialized before each test
    with app.test_client() as client:
        yield client


def test_login_success(client):
    """
    Test successful login.
    """
    response = client.post(
        "/login", json={"email": "student@example.com", "password": "Password123"}
    )
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_failure(client):
    """
    Test login failure with incorrect password.
    """
    response = client.post(
        "/login", json={"email": "student@example.com", "password": "WrongPassword"}
    )
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials"
