import io
from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.api import items as items_module
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
        "status": "expired",
        "days_until_expiry": (date(2020, 4, 4) - date.today()).days,
        "photo_path": None,
    }


def test_post_item_bad_quantity(fresh_repository):
    payload = {
        "name": "test_name",
        "quantity": 0,
        "expiry_date": "2020-04-04",
    }
    res = client.post("/items", json=payload)

    assert res.status_code == 422


def test_list_items(fresh_repository, tomorrow):
    item1 = create_item()
    item2 = create_item(name="test_name2")
    item3 = create_item(name="test_name3", user_id=2)
    fresh_repository.add_item(item1)
    fresh_repository.add_item(item2)
    fresh_repository.add_item(item3)
    res = client.get("/items")

    assert res.status_code == 200
    assert len(res.json()) == 2

    assert res.json() == [
        {
            "id": 1,
            "name": "test_item",
            "quantity": 1,
            "added_date": date.today().isoformat(),
            "expiry_date": tomorrow.isoformat(),
            "user_id": 1,
            "status": "expiring_soon",
            "days_until_expiry": 1,
            "photo_path": None,
        },
        {
            "id": 2,
            "name": "test_name2",
            "quantity": 1,
            "added_date": date.today().isoformat(),
            "expiry_date": tomorrow.isoformat(),
            "user_id": 1,
            "status": "expiring_soon",
            "days_until_expiry": 1,
            "photo_path": None,
        },
    ]


def test_get_item_successful(seeded_item, tomorrow):
    res = client.get("/items/1")

    assert res.status_code == 200
    assert res.json() == {
        "id": 1,
        "name": "test_item",
        "quantity": 1,
        "added_date": date.today().isoformat(),
        "expiry_date": tomorrow.isoformat(),
        "user_id": 1,
        "status": "expiring_soon",
        "days_until_expiry": 1,
        "photo_path": None,
    }


def test_get_item_id_not_found(fresh_repository):
    res = client.get("/items/99")
    assert res.status_code == 404
    assert res.json() == {"detail": "Item 99 not found"}


def test_delete_item(seeded_item, tomorrow):
    res = client.delete("/items/1")

    assert res.status_code == 204


def test_delete_item_not_found(fresh_repository):
    res = client.delete("/items/99")

    assert res.status_code == 404
    assert res.json() == {"detail": "Item 99 not found"}


def test_update_item(seeded_item, tomorrow):
    tomorrow = tomorrow + timedelta(days=1)
    payload = {
        "name": "change_name",
        "quantity": 5,
        "expiry_date": tomorrow.isoformat(),
    }
    res = client.put("/items/1", json=payload)
    assert res.status_code == 200
    assert res.json() == {
        "id": 1,
        "name": "change_name",
        "quantity": 5,
        "added_date": date.today().isoformat(),
        "expiry_date": tomorrow.isoformat(),
        "user_id": 1,
        "status": "expiring_soon",
        "days_until_expiry": 2,
        "photo_path": None,
    }


def test_update_item_not_found(fresh_repository):
    res = client.put("/items/99", json={"name": "change_name"})
    assert res.status_code == 404
    assert res.json() == {"detail": "Item 99 not found"}


def test_get_item_owned_by_another_user(fresh_repository):
    other_users_item = create_item(user_id=2)
    fresh_repository.add_item(other_users_item)

    res = client.get(f"/items/{other_users_item.id}")

    assert res.status_code == 404
    assert res.json() == {"detail": f"Item {other_users_item.id} not found"}


def test_delete_item_owned_by_another_user(fresh_repository):
    other_users_item = create_item(user_id=2)
    fresh_repository.add_item(other_users_item)

    res = client.delete(f"/items/{other_users_item.id}")

    assert res.status_code == 404
    assert res.json() == {"detail": f"Item {other_users_item.id} not found"}


def test_update_item_owned_by_another_user(fresh_repository):
    other_users_item = create_item(user_id=2)
    fresh_repository.add_item(other_users_item)

    res = client.put(f"/items/{other_users_item.id}", json={"name": "hijacked"})

    assert res.status_code == 404
    assert res.json() == {"detail": f"Item {other_users_item.id} not found"}


def test_get_item_sorted_by_expire_days(fresh_repository):
    expired_item = create_item(
        name="expired_item", expiry_date=date.today() - timedelta(days=1)
    )
    item = create_item()
    fresh_repository.add_item(item)
    fresh_repository.add_item(expired_item)
    res = client.get("/items/")

    assert res.status_code == 200
    assert res.json()[0]["name"] == "expired_item"


def test_upload_photo_success(seeded_item, tmp_path, monkeypatch):
    monkeypatch.setattr(items_module, "UPLOAD_DIR", tmp_path)
    file_content = b"fake image bytes"

    res = client.post(
        "/items/1/photo",
        files={"image": ("photo.jpg", io.BytesIO(file_content), "image/jpeg")},
    )

    assert res.status_code == 200
    data = res.json()
    assert data["photo_path"].startswith("uploads/")
    assert data["photo_path"].endswith(".jpg")

    saved_files = list(tmp_path.iterdir())
    assert len(saved_files) == 1
    assert saved_files[0].read_bytes() == file_content


def test_upload_photo_missing_filename(seeded_item, tmp_path, monkeypatch):
    monkeypatch.setattr(items_module, "UPLOAD_DIR", tmp_path)

    res = client.post(
        "/items/1/photo",
        files={"image": ("", io.BytesIO(b"data"), "image/jpeg")},
    )

    # FastAPI itself rejects an empty filename during multipart parsing,
    # before _validate_image's own filename check ever runs.
    assert res.status_code == 422


def test_upload_photo_invalid_extension(seeded_item, tmp_path, monkeypatch):
    monkeypatch.setattr(items_module, "UPLOAD_DIR", tmp_path)

    res = client.post(
        "/items/1/photo",
        files={"image": ("malware.exe", io.BytesIO(b"data"), "image/jpeg")},
    )

    assert res.status_code == 400
    assert list(tmp_path.iterdir()) == []


def test_upload_photo_invalid_content_type(seeded_item, tmp_path, monkeypatch):
    monkeypatch.setattr(items_module, "UPLOAD_DIR", tmp_path)

    res = client.post(
        "/items/1/photo",
        files={"image": ("photo.jpg", io.BytesIO(b"data"), "text/plain")},
    )

    assert res.status_code == 400
    assert list(tmp_path.iterdir()) == []


def test_upload_photo_too_large(seeded_item, tmp_path, monkeypatch):
    monkeypatch.setattr(items_module, "UPLOAD_DIR", tmp_path)
    monkeypatch.setattr(items_module, "MAX_FILE_SIZE", 10)

    res = client.post(
        "/items/1/photo",
        files={
            "image": ("photo.jpg", io.BytesIO(b"more than ten bytes"), "image/jpeg")
        },
    )

    assert res.status_code == 413
    assert list(tmp_path.iterdir()) == []


def test_upload_photo_not_found(fresh_repository):
    res = client.post(
        "/items/99/photo",
        files={"image": ("photo.jpg", io.BytesIO(b"data"), "image/jpeg")},
    )

    assert res.status_code == 404
    assert res.json() == {"detail": "Item 99 not found"}


def test_upload_photo_owned_by_another_user(fresh_repository):
    other_users_item = create_item(user_id=2)
    fresh_repository.add_item(other_users_item)

    res = client.post(
        f"/items/{other_users_item.id}/photo",
        files={"image": ("photo.jpg", io.BytesIO(b"data"), "image/jpeg")},
    )

    assert res.status_code == 404
    assert res.json() == {"detail": f"Item {other_users_item.id} not found"}
