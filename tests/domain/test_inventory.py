from datetime import date

from app.domain.inventory import Item


class TestInventory:

    def setup_method(self):
        self.added = date(2026, 8, 25)
        self.today = date(2026, 8, 30)
        self.expiry = date(2026, 9, 2)
        self.item = Item("test_item", self.added, self.expiry)

    def test_days_until_expiry_count_day_from_today(self):
        assert self.item.days_until_expiry(self.today) == 3

    def test_create_item(self):
        assert self.item.name == "test_item"

