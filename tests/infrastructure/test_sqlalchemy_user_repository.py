import pytest

from app.domain.exceptions import UserNotFound
from app.infrastructure.user_repository import SQLAlchemyUserRepository
from tests.domain.utils import create_user


def test_add_user(db_session):
    user = create_user()
    repository = SQLAlchemyUserRepository(db_session)
    added_user = repository.add_user(user)

    assert user is added_user
    assert user.id is not None


def test_get_user(db_session):
    user = create_user()
    repository = SQLAlchemyUserRepository(db_session)
    repository.add_user(user)
    retrieved = repository.get_user(user.id)

    assert user.name == retrieved.name
    assert user.id == retrieved.id
    assert user.email == retrieved.email


def test_get_user_not_found(db_session):
    repository = SQLAlchemyUserRepository(db_session)
    with pytest.raises(UserNotFound):
        repository.get_user(99)


def test_get_by_email(db_session):
    user = create_user()
    repository = SQLAlchemyUserRepository(db_session)
    repository.add_user(user)
    retrieved = repository.get_by_email(user.email)

    assert user.name == retrieved.name
    assert user.id == retrieved.id


def test_get_user_by_email_not_found(db_session):
    repository = SQLAlchemyUserRepository(db_session)
    with pytest.raises(UserNotFound):
        repository.get_by_email("none@example.com")
