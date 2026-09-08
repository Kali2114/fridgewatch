class User:
    def __init__(self, name, email, hashed_password, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = True
