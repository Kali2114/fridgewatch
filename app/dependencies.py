from collections.abc import Iterator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app import security
from app.domain.exceptions import UserNotFound
from app.domain.user import User
from app.infrastructure.database import SessionLocal
from app.infrastructure.repository import SQLAlchemyItemRepository
from app.infrastructure.user_repository import SQLAlchemyUserRepository


def get_repository() -> Iterator[SQLAlchemyItemRepository]:
    session = SessionLocal()
    try:
        repository = SQLAlchemyItemRepository(session)
        yield repository
    finally:
        session.close()


def get_user_repository() -> Iterator[SQLAlchemyUserRepository]:
    session = SessionLocal()
    try:
        repository = SQLAlchemyUserRepository(session)
        yield repository
    finally:
        session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> User:
    try:
        user_id = security.decode_access_token(token)
        user = repository.get_user(user_id)
        return user
    except (UserNotFound, JWTError):
        raise HTTPException(status_code=401, detail="Invalid credentials")
