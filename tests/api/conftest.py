from datetime import date, timedelta

import pytest

from app.dependencies import get_repository
from app.domain.repository import InMemoryItemRepository
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
