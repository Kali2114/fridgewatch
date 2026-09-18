from datetime import date, timedelta

from app.domain.inventory import Item
from app.domain.recipe import Recipe
from app.domain.user import User


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


def create_user(**kwargs):
    payload = {
        "name": "test_user",
        "email": "test@example.com",
        "hashed_password": "test_password",
    }
    payload.update(kwargs)
    return User(**payload)


def create_recipe(**kwargs):
    payload = {
        "name": "test_recipe",
        "required_ingredients": ["eggs", "butter"],
    }
    payload.update(kwargs)
    return Recipe(**payload)
