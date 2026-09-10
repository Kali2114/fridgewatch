import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.dependencies as dependencies
from app.dependencies import get_current_user, get_repository, get_user_repository
from app.domain.user_repository import InMemoryUserRepository
from app.infrastructure.repository import SQLAlchemyItemRepository
from app.security import create_access_token
from tests.domain.utils import create_user


def test_get_repository_yields_and_closes_session(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(dependencies, "SessionLocal", sessionmaker(bind=engine))

    generator = get_repository()
    repository = next(generator)

    assert isinstance(repository, SQLAlchemyItemRepository)

    with pytest.raises(StopIteration):
        next(generator)


def test_get_user_repository_returns_the_shared_instance():
    assert isinstance(get_user_repository(), InMemoryUserRepository)


def test_get_current_user_success():
    repository = InMemoryUserRepository()
    user = repository.add_user(create_user())
    token = create_access_token(user.id)

    result = get_current_user(token=token, repository=repository)

    assert result is user


def test_get_current_user_invalid_token():
    repository = InMemoryUserRepository()

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="not-a-real-token", repository=repository)

    assert exc_info.value.status_code == 401


def test_get_current_user_unknown_user_id():
    repository = InMemoryUserRepository()
    token = create_access_token(999)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token, repository=repository)

    assert exc_info.value.status_code == 401
