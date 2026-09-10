from app.infrastructure.user_repository import SQLAlchemyUserRepository
from tests.domain.utils import create_user


def test_add_user(db_session):
    user = create_user()
    repository = SQLAlchemyUserRepository(db_session)
    added_user = repository.add_user(user)

    assert user is added_user
    assert user.id is not None
