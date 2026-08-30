from enum import Enum

class ExpiryStatus(Enum):
    FRESH = "fresh"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"



class Item:
    def __init__(self, name, added_date, expiry_date):
        self.name = name
        self.added_date = added_date
        self.expiry_date = expiry_date

    def days_until_expiry(self, today):
        difference = self.expiry_date - today
        return difference.days

    def status(self, today):
        difference = self.days_until_expiry(today)
        if difference < 0:
            return ExpiryStatus.EXPIRED
        elif difference <= 2:
            return ExpiryStatus.EXPIRING_SOON
        else:
            return ExpiryStatus.FRESH