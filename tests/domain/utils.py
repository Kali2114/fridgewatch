from datetime import date, timedelta

from app.domain.inventory import Item


def create_item(**kwargs):
    payload = {
        "name": "test_item",
        "quantity": 1,
        "added_date": date.today(),
        "expiry_date": date.today() + timedelta(days=1),
        "user_id": 1,
    }
    payload.update(kwargs)
    return Item(**payload)