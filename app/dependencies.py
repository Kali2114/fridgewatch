from collections.abc import Iterator

from app.domain.user_repository import InMemoryUserRepository
from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import SQLAlchemyItemRepository


def get_repository() -> Iterator[SQLAlchemyItemRepository]:
    session = SessionLocal()
    try:
        repository = SQLAlchemyItemRepository(session)
        yield repository
    finally:
        session.close()


user_repository = InMemoryUserRepository()


def get_user_repository() -> InMemoryUserRepository:
    return user_repository
