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
            raise ItemNotFound(f"Item {item_id} not found")