import pytest

from app.domain.exceptions import ItemNotFound
from app.infrastructure.repository import SQLAlchemyItemRepository
from tests.domain.utils import create_item


class TestSQLAlchemyItemRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = SQLAlchemyItemRepository(db_session)

    def test_add_item(self):
        item = create_item()
        added_item = self.repository.add_item(item)

        assert item is added_item
        assert item.id is not None

    def test_get_item(self):
        item = create_item()
        self.repository.add_item(item)
        retrieved = self.repository.get_item(item.id)

        assert retrieved.name == item.name
        assert retrieved.id == item.id

    def test_get_item_not_found(self):
        with pytest.raises(ItemNotFound):
            self.repository.get_item(99)

    def test_item_photo_path_round_trips(self):
        item = create_item(photo_path="uploads/item1.jpg")
        self.repository.add_item(item)
        retrieved = self.repository.get_item(item.id)

        assert retrieved.photo_path == "uploads/item1.jpg"

    def test_list_for_user(self):
        item1 = create_item(name="item1")
        item2 = create_item(name="item2")
        self.repository.add_item(item1)
        self.repository.add_item(item2)
        user_list = self.repository.list_for_user(1)

        assert [i.name for i in user_list] == ["item1", "item2"]
        assert len(user_list) == 2

    def test_list_for_no_exist_id_return_empty_list(self):
        result = self.repository.list_for_user(9999)
        assert result == []

    def test_delete_item(self):
        item = create_item()
        self.repository.add_item(item)

        self.repository.delete_item(item.id)

        with pytest.raises(ItemNotFound):
            self.repository.get_item(item.id)

    def test_delete_item_not_found(self):
        with pytest.raises(ItemNotFound):
            self.repository.delete_item(99)

    def test_update_item(self):
        item = create_item()
        self.repository.add_item(item)
        payload = {
            "name": "Updated item",
            "quantity": 10,
        }
        updated_item = self.repository.update_item(item.id, payload)

        assert updated_item.id == item.id
        assert updated_item.name == payload["name"]
        assert updated_item.quantity == payload["quantity"]

    def test_update_item_invalid_quantity(self):
        item = create_item()
        self.repository.add_item(item)
        payload = {
            "quantity": -5,
        }
        with pytest.raises(ValueError):
            self.repository.update_item(item.id, payload)

    def test_update_item_not_found(self):
        with pytest.raises(ItemNotFound):
            self.repository.update_item(10, {})

    def test_list_all(self):
        self.repository.add_item(create_item())
        self.repository.add_item(create_item(name="another_item", user_id=2))
        result = self.repository.list_all()

        assert len(result) == 2
        assert [item.user_id for item in result] == [1, 2]
