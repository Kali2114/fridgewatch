from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_user(user_fresh_repository):
    payload = {
        "name": "test_name",
        "email": "test@example.com",
        "password": "secret123",
    }
    res = client.post("/auth/register", json=payload)

    assert res.status_code == 201
    assert res.json()["name"] == payload["name"]
    assert res.json()["email"] == payload["email"]
