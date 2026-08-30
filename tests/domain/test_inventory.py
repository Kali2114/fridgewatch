from datetime import date, timedelta

import pytest

from app.domain.inventory import ExpiryStatus, Item


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

    @pytest.mark.parametrize(
        "days_out, expected",
        [
            (10, ExpiryStatus.FRESH),
            (3, ExpiryStatus.FRESH),          # just outside the 2-day window
            (2, ExpiryStatus.EXPIRING_SOON),  # boundary
            (1, ExpiryStatus.EXPIRING_SOON),
            (0, ExpiryStatus.EXPIRING_SOON),  # expires today, not expired yet
            (-1, ExpiryStatus.EXPIRED),
        ],
    )
    def test_status(self, days_out, expected):
        item = Item("x", self.added, self.today + timedelta(days=days_out))
        assert item.status(self.today) == expected


