from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.main import app
from tests.domain.utils import create_item

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


def test_list_items(fresh_repository):
    item1 = create_item()
    item2 = create_item(name="test_name2")
    item3 = create_item(name="test_name3", user_id=2)
    fresh_repository.add_item(item1)
    fresh_repository.add_item(item2)
    fresh_repository.add_item(item3)
    res = client.get("/items")

    assert res.status_code == 200
    assert len(res.json()) == 2
    date_dict = date.today() + timedelta(days=1)

    assert res.json() == [
        {
            "id": 1,
            "name": "test_item",
            "quantity": 1,
            "added_date": date.today().isoformat(),
            "expiry_date": date_dict.isoformat(),
            "user_id": 1,
        },
        {
            "id": 2,
            "name": "test_name2",
            "quantity": 1,
            "added_date": date.today().isoformat(),
            "expiry_date": date_dict.isoformat(),
            "user_id": 1,
        },
    ]
