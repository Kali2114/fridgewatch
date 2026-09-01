import pytest

from app.domain.exceptions import ItemNotFound
from app.domain.repository import InMemoryItemRepository

from . import utils


class TestInMemoryItemRepository:

    def setup_method(self):
        self.item = utils.create_item()
        self.repository = InMemoryItemRepository()
        self.added = self.repository.add_item(self.item)

    def test_add_item(self):
        assert self.added is self.item
        assert self.item.id == 1

    def test_get_item(self):
        retrieved = self.repository.get_item(1)
        assert retrieved is self.item

    def test_get_item_not_found(self):
        with pytest.raises(ItemNotFound):
            self.repository.get_item(99)

    def test_second_add_gets_next_id(self):
        item = self.repository.add_item(utils.create_item(name="test_item2"))
        assert item.id == 2

    def test_list_for_user(self):
        self.repository.add_item(utils.create_item(user_id=2, name="test_item2"))
        mine = self.repository.add_item(utils.create_item(name="test_item2"))
        result = self.repository.list_for_user(1)

        assert len(result) == 2
        assert set(result) == {self.item, mine}

    def test_list_for_no_exist_id_return_empty_list(self):
        result = self.repository.list_for_user(9999)
        assert result == []

    def test_delete_item(self):
        self.repository.delete_item(1)

        with pytest.raises(ItemNotFound):
            self.repository.get_item(1)

    def test_delete_item_not_found(self):
        with pytest.raises(ItemNotFound):
            self.repository.delete_item(99)

    def test_update_item(self):
        payload = {
            "name": "change_name",
            "quantity": 4,
        }
        self.repository.update_item(1, payload)

        assert self.repository.get_item(1).name == payload["name"]
        assert self.repository.get_item(1).quantity == 4

    def test_update_invalid_quantity(self):
        with pytest.raises(ValueError):
            self.repository.update_item(1, {"quantity": -4})

    def test_update_item_not_found(self):
        with pytest.raises(ItemNotFound):
            self.repository.update_item(2, {"name": "change_name"})


