import pytest
from fastapi.testclient import TestClient
from datetime import date

from app.main import app


client = TestClient(app)


def test_post_item(fresh_repository):
    payload = {
        "name": "test_name",
        "quantity": 1,
        "expiry_date": "2020-04-04",
    }
    res = client.post("/items", json=payload)
    assert res.status_code == 201
    assert res.json() == {
        "id": 1,
        "name": "test_name",
        "quantity": 1,
        "expiry_date": "2020-04-04",
        "added_date": date.today().isoformat(),
        "user_id": 1,
    }

def test_post_item_bad_quantity(fresh_repository):
    payload = {
        "name": "test_name",
        "quantity": 0,
        "expiry_date": "2020-04-04",
    }
    res = client.post("/items", json=payload)

    assert res.status_code == 422
