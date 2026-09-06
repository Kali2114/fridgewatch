from app.infrastructure.repository import SQLAlchemyItemRepository
from tests.domain.utils import create_item


def test_add_item(db_session):
    item = create_item()
    repository = SQLAlchemyItemRepository(db_session)
    added_item = repository.add_item(item)

    assert item is added_item
    assert item.id is not None
