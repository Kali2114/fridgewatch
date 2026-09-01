from enum import Enum

class ExpiryStatus(Enum):
    FRESH = "fresh"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"



class Item:
    def __init__(self, user_id, name, quantity, added_date, expiry_date, id=None):
        self.name = name
        self.quantity = quantity
        self.added_date = added_date
        self.expiry_date = expiry_date
        self.user_id = user_id
        self.id = id

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("quantity must be positive")
        self._quantity = value

    def days_until_expiry(self, today):
        difference = self.expiry_date - today
        return difference.days

    def status(self, today):
        days = self.days_until_expiry(today)
        if days < 0:
            return ExpiryStatus.EXPIRED
        elif days <= 2:
            return ExpiryStatus.EXPIRING_SOON
        else:
            return ExpiryStatus.FRESH