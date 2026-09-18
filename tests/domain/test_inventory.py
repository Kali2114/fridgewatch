from datetime import date, timedelta

import pytest

from app.domain.inventory import ExpiryStatus, items_expiring_soon
from tests.domain.utils import create_item


class TestInventory:
    def setup_method(self):
        self.today = date(2026, 8, 30)
        self.item = create_item()

    def test_days_until_expiry_count_day_from_today(self):
        item = create_item(expiry_date=self.today + timedelta(days=3))
        assert item.days_until_expiry(self.today) == 3

    def test_create_item(self):
        assert self.item.name == "test_item"
        assert self.item.user_id == 1
        assert self.item.id is None

    @pytest.mark.parametrize(
        "days_out, expected",
        [
            (10, ExpiryStatus.FRESH),
            (3, ExpiryStatus.FRESH),  # just outside the 2-day window
            (2, ExpiryStatus.EXPIRING_SOON),  # boundary
            (1, ExpiryStatus.EXPIRING_SOON),
            (0, ExpiryStatus.EXPIRING_SOON),  # expires today, not expired yet
            (-1, ExpiryStatus.EXPIRED),
        ],
    )
    def test_status(self, days_out, expected):
        item = create_item(expiry_date=self.today + timedelta(days=days_out))
        assert item.status(self.today) == expected

    def test_non_positive_quantity_raises(self):
        with pytest.raises(ValueError):
            create_item(quantity=0)

    def test_items_expiring_soon(self):
        today = date.today()

        expiring_soon = create_item(
            name="expiring_soon",
            expiry_date=today + timedelta(days=1),
        )
        expires_later = create_item(
            name="expires_later",
            expiry_date=today + timedelta(days=5),
        )
        expired = create_item(
            name="expired",
            expiry_date=today - timedelta(days=1),
        )

        result = items_expiring_soon(
            [expiring_soon, expires_later, expired],
            today,
            within_days=2,
        )

        assert result == [expiring_soon]
