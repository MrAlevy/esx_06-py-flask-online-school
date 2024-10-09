import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_rate_limiting(client):
    """
    Test that rate limiting is enforced after exceeding the allowed number of requests.
    """
    for _ in range(5):
        response = client.post(
            "/login", json={"email": "student@example.com", "password": "Password123"}
        )
    response = client.post(
        "/login", json={"email": "student@example.com", "password": "Password123"}
    )
    assert response.status_code == 429  # Too Many Requests
