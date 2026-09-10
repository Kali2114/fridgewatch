from app.domain.exceptions import EmailAlreadyRegistered, UserNotFound
from app.domain.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users: dict[int, User] = {}
        self.next_index = 1

    def _find_by_email(self, email: str) -> User | None:
        for value in self.users.values():
            if value.email == email:
                return value
        return None

    def add_user(self, user: User) -> User:
        if self._find_by_email(user.email) is not None:
            raise EmailAlreadyRegistered(f"Email {user.email} already registered")
        user.id = self.next_index
        self.users[user.id] = user
        self.next_index += 1
        return user

    def get_user(self, user_id: int) -> User:
        try:
            return self.users[user_id]
        except KeyError:
            raise UserNotFound(f"User with id {user_id} not found")

    def get_by_email(self, email: str) -> User:
        value = self._find_by_email(email)
        if value is None:
            raise UserNotFound(f"User with email {email} not found")
        return value
