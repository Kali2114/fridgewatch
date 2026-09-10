from fastapi.testclient import TestClient

from app.main import app
from app.security import hash_password
from tests.domain.utils import create_user

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


def test_register_user_already_exists(user_fresh_repository):
    payload = {
        "name": "test_name",
        "email": "test@example.com",
        "password": "secret123",
    }
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)

    assert res.status_code == 409
    assert res.json() == {"detail": "Email test@example.com already registered"}


def test_login_user(user_fresh_repository):
    user = create_user(hashed_password=hash_password("secret123"))
    user_fresh_repository.add_user(user)
    payload = {
        "email": user.email,
        "password": "secret123",
    }
    res = client.post("/auth/login", json=payload)

    assert res.status_code == 200
    assert "access_token" in res.json()
    assert isinstance(res.json()["access_token"], str)
    assert res.json()["access_token"]


def test_login_user_not_exist(user_fresh_repository):
    payload = {
        "email": "not_exist@example.com",
        "password": "not_exist",
    }

    res = client.post("/auth/login", json=payload)
    assert res.status_code == 401
    assert "access_token" not in res.json()
