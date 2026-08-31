import pytest

from app.domain.repository import InMemoryItemRepository
from . import utils
from app.domain.exceptions import ItemNotFound

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
