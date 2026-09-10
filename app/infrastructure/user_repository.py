from app.domain.exceptions import UserNotFound
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

    def get_user(self, user_id: int) -> User:
        model = self.session.get(UserModel, user_id)
        if model is None:
            raise UserNotFound(f"User with id {user_id} not found")
        return self._to_domain(model)

    @staticmethod
    def _to_domain(user: UserModel) -> User:
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
        )
