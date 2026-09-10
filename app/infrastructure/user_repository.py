from app.domain.user import User
from app.infrastructure.models import UserModel


class SQLAlchemyUserRepository:
    def __init__(self, session):
        self.session = session

    def add_user(self, user: User) -> User:
        model = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )
        self.session.add(model)
        self.session.commit()
        user.id = model.id
        return user
