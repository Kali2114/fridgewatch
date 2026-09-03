import pytest

from app.dependencies import get_repository
from app.domain.repository import InMemoryItemRepository
from app.main import app


@pytest.fixture
def fresh_repository():
    repository = InMemoryItemRepository()

    app.dependency_overrides[get_repository] = lambda: repository

    yield repository

    app.dependency_overrides.clear()