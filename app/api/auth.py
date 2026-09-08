from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import get_user_repository
from app.domain.user import User
from app.schemas import UserCreate, UserRead
from app.security import hash_password

router = APIRouter()


@router.post(
    "/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate, repository=Depends(get_user_repository)):
    hashed = hash_password(user.password)
    user_created = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed,
    )
    new_user = repository.add_user(user_created)
    return new_user
