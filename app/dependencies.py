from collections.abc import Iterator

from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import SQLAlchemyItemRepository


def get_repository() -> Iterator[SQLAlchemyItemRepository]:
    session = SessionLocal()
    try:
        repository = SQLAlchemyItemRepository(session)
        yield repository
    finally:
        session.close()
