from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_user_repository
from app.domain.exceptions import UserNotFound
from app.domain.user import User
from app.schemas import TokenResponse, UserCreate, UserLogin, UserRead
from app.security import create_access_token, hash_password, verify_password

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


@router.post(
    "/auth/login", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
def login_user(user: UserLogin, repository=Depends(get_user_repository)):
    try:
        found_user = repository.get_by_email(user.email)
    except UserNotFound:
        found_user = None

    if found_user is None or not verify_password(
        user.password, found_user.hashed_password
    ):
        raise HTTPException(401, detail="Invalid credentials")

    token = create_access_token(found_user.id)
    return {"access_token": token, "token_type": "bearer"}
