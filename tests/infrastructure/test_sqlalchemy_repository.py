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


def test_list_for_user(db_session):
    item1 = create_item(name="item1")
    item2 = create_item(name="item2")
    repository = SQLAlchemyItemRepository(db_session)
    repository.add_item(item1)
    repository.add_item(item2)
    user_list = repository.list_for_user(1)

    assert [i.name for i in user_list] == ["item1", "item2"]
    assert len(user_list) == 2


def test_list_for_no_exist_id_return_empty_list(db_session):
    repository = SQLAlchemyItemRepository(db_session)
    result = repository.list_for_user(9999)
    assert result == []


def test_delete_item(db_session):
    item = create_item()
    repository = SQLAlchemyItemRepository(db_session)
    repository.add_item(item)

    repository.delete_item(item.id)

    with pytest.raises(ItemNotFound):
        repository.get_item(item.id)


def test_delete_item_not_found(db_session):
    repository = SQLAlchemyItemRepository(db_session)
    with pytest.raises(ItemNotFound):
        repository.delete_item(99)


def test_update_item(db_session):
    item = create_item()
    repository = SQLAlchemyItemRepository(db_session)
    repository.add_item(item)
    payload = {
        "name": "Updated item",
        "quantity": 10,
    }
    updated_item = repository.update_item(item.id, payload)

    assert updated_item.id == item.id
    assert updated_item.name == payload["name"]
    assert updated_item.quantity == payload["quantity"]


def test_update_item_invalid_quantity(db_session):
    item = create_item()
    repository = SQLAlchemyItemRepository(db_session)
    repository.add_item(item)
    payload = {
        "quantity": -5,
    }
    with pytest.raises(ValueError):
        repository.update_item(item.id, payload)


def test_update_item_not_found(db_session):
    repository = SQLAlchemyItemRepository(db_session)
    with pytest.raises(ItemNotFound):
        repository.update_item(10, {})
