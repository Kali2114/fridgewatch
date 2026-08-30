

class Item:
    def __init__(self, name, added_date, expiry_date):
        self.name = name
        self.added_date = added_date
        self.expiry_date = expiry_date

    def days_until_expiry(self, today):
        difference = self.expiry_date - today
        return difference.days