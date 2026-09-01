from app.domain.exceptions import ItemNotFound


class InMemoryItemRepository:
    def __init__(self):
        self.items = {}
        self._next_id = 1

    def add_item(self, item):
        item.id = self._next_id
        self.items[item.id] = item
        self._next_id += 1
        return item

    def get_item(self, item_id):
        try:
            return self.items[item_id]
        except KeyError:
            raise ItemNotFound(f"Item {item_id} not found") from None

    def list_for_user(self, user_id):
        return [i for i in self.items.values() if i.user_id == user_id]

    def delete_item(self, item_id):
        try:
            del self.items[item_id]
        except KeyError:
            raise ItemNotFound(f"Item {item_id} not found") from None

    def update_item(self, item_id, payload):
        item = self.get_item(item_id)
        for key, value in payload.items():
            setattr(item, key, value)
        return item