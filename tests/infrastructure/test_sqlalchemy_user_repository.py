import pytest

from app.domain.exceptions import UserNotFound
from app.infrastructure.user_repository import SQLAlchemyUserRepository
from tests.domain.utils import create_user


class TestSQLAlchemyUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = SQLAlchemyUserRepository(db_session)

    def test_add_user(self):
        user = create_user()
        added_user = self.repository.add_user(user)

        assert user is added_user
        assert user.id is not None

    def test_get_user(self):
        user = create_user()
        self.repository.add_user(user)
        retrieved = self.repository.get_user(user.id)

        assert user.name == retrieved.name
        assert user.id == retrieved.id
        assert user.email == retrieved.email

    def test_get_user_not_found(self):
        with pytest.raises(UserNotFound):
            self.repository.get_user(99)

    def test_get_by_email(self):
        user = create_user()
        self.repository.add_user(user)
        retrieved = self.repository.get_by_email(user.email)

        assert user.name == retrieved.name
        assert user.id == retrieved.id

    def test_get_user_by_email_not_found(self):
        with pytest.raises(UserNotFound):
            self.repository.get_by_email("none@example.com")
