import pytest

from app.domain.exceptions import ItemNotFound
from app.infrastructure.repository import SQLAlchemyItemRepository
from tests.domain.utils import create_item


def test_add_item(db_session):
    item = create_item()
    repository = SQLAlchemyItemRepository(db_session)
    added_item = repository.add_item(item)

    assert item is added_item
    assert item.id is not None


def test_get_item(db_session):
    item = create_item()
    repository = SQLAlchemyItemRepository(db_session)
    repository.add_item(item)
    retrieved = repository.get_item(item.id)

    assert retrieved.name == item.name
    assert retrieved.id == item.id


def test_get_item_not_found(db_session):
    repository = SQLAlchemyItemRepository(db_session)
    with pytest.raises(ItemNotFound):
        repository.get_item(99)
