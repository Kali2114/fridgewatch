from app.domain.repository import InMemoryItemRepository

repository = InMemoryItemRepository()


def get_repository() -> InMemoryItemRepository:
    return repository