from typing import Any

from app.domain.exceptions import ItemNotFound
from app.domain.inventory import Item


class InMemoryItemRepository:
    def __init__(self) -> None:
        self.items: dict[int, Item] = {}
        self._next_id = 1

    def add_item(self, item: Item) -> Item:
        item.id = self._next_id
        self.items[item.id] = item
        self._next_id += 1
        return item

    def get_item(self, item_id: int) -> Item:
        try:
            return self.items[item_id]
        except KeyError:
            raise ItemNotFound(f"Item {item_id} not found") from None

    def list_for_user(self, user_id: int) -> list[Item]:
        return [i for i in self.items.values() if i.user_id == user_id]

    def delete_item(self, item_id: int) -> None:
        try:
            del self.items[item_id]
        except KeyError:
            raise ItemNotFound(f"Item {item_id} not found") from None

    def update_item(self, item_id: int, payload: dict[str, Any]) -> Item:
        item = self.get_item(item_id)
        for key, value in payload.items():
            setattr(item, key, value)
        return item
