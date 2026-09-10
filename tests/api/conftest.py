from datetime import date, timedelta

import pytest

from app.dependencies import get_current_user, get_repository, get_user_repository
from app.domain.repository import InMemoryItemRepository
from app.domain.user import User
from app.domain.user_repository import InMemoryUserRepository
from app.main import app
from tests.domain.utils import create_item


@pytest.fixture
def fresh_repository():
    repository = InMemoryItemRepository()

    app.dependency_overrides[get_repository] = lambda: repository

    yield repository

    app.dependency_overrides.clear()


@pytest.fixture
def tomorrow():
    return date.today() + timedelta(days=1)


@pytest.fixture
def seeded_item(fresh_repository):
    item = create_item()
    fresh_repository.add_item(item)
    return item


@pytest.fixture
def user_fresh_repository():
    repository = InMemoryUserRepository()

    app.dependency_overrides[get_user_repository] = lambda: repository

    yield repository

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def current_user():
    user = User(id=1, name="test_user", email="test@example.com", hashed_password="x")

    app.dependency_overrides[get_current_user] = lambda: user

    yield user

    app.dependency_overrides.clear()
