import pytest

from app.domain.exceptions import EmailAlreadyRegistered, UserNotFound
from app.domain.user_repository import InMemoryUserRepository

from . import utils


class TestUserRepository:

    def setup_method(self):
        self.user = utils.create_user()
        self.repository = InMemoryUserRepository()
        self.added = self.repository.add_user(self.user)

    def test_add_user(self):
        assert self.added.id == 1
        assert self.user is self.added

    def test_add_user_email_exists(self):
        with pytest.raises(EmailAlreadyRegistered):
            self.repository.add_user(utils.create_user())

    def test_get_user_by_id(self):
        retrieved = self.repository.get_user(1)
        assert retrieved is self.added

    def test_get_user_by_id_not_found(self):
        with pytest.raises(UserNotFound):
            self.repository.get_user(99)

    def test_second_add_gets_next_id(self):
        new_user = utils.create_user(name="second", email="second@example.com")
        self.repository.add_user(new_user)
        assert new_user.id == 2

    def test_get_user_by_email(self):
        retrieved = self.repository.get_by_email("test@example.com")
        assert retrieved is self.added

    def test_get_user_by_email_not_found(self):
        with pytest.raises(UserNotFound):
            self.repository.get_by_email("wrong@wrongly.uv")
