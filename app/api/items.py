from datetime import date
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.dependencies import get_current_user, get_repository
from app.domain.exceptions import ItemNotFound
from app.domain.inventory import Item
from app.domain.user import User
from app.schemas import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
UPLOAD_DIR = Path("static/uploads")


def _get_owned_item(item_id: int, repository, current_user: User) -> Item:
    item = repository.get_item(item_id)
    if item.user_id != current_user.id:
        raise ItemNotFound(f"Item {item_id} not found")
    return item


def _item_to_read(item: Item) -> ItemRead:
    today = date.today()
    return ItemRead(
        id=item.id,
        name=item.name,
        quantity=item.quantity,
        expiry_date=item.expiry_date,
        added_date=item.added_date,
        user_id=item.user_id,
        status=item.status(today),
        days_until_expiry=item.days_until_expiry(today),
        photo_path=item.photo_path,
    )


@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    repository=Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> ItemRead:
    item_created = Item(
        name=item.name,
        quantity=item.quantity,
        expiry_date=item.expiry_date,
        user_id=current_user.id,
        added_date=date.today(),
    )
    repository.add_item(item_created)
    new_item = _item_to_read(item_created)
    return new_item


@router.get("/items", response_model=list[ItemRead], status_code=status.HTTP_200_OK)
def list_items(
    repository=Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> list[ItemRead]:
    items = repository.list_for_user(user_id=current_user.id)
    items_for_return = [_item_to_read(item) for item in items]
    return sorted(items_for_return, key=lambda x: x.days_until_expiry)


@router.get("/items/{item_id}", response_model=ItemRead, status_code=status.HTTP_200_OK)
def read_item(
    item_id: int,
    repository=Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> ItemRead:
    item = _get_owned_item(item_id, repository, current_user)
    return _item_to_read(item)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    repository=Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> None:
    _get_owned_item(item_id, repository, current_user)
    repository.delete_item(item_id)


@router.put("/items/{item_id}", response_model=ItemRead, status_code=status.HTTP_200_OK)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    repository=Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> ItemRead:
    _get_owned_item(item_id, repository, current_user)
    payload = item_update.model_dump(exclude_unset=True)
    updated_item = repository.update_item(item_id, payload)
    return _item_to_read(updated_item)


def _validate_image(image: UploadFile) -> str:

    extension = Path(image.filename).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file extension",
        )

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type",
        )

    if image.size is not None and image.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large",
        )

    return extension


def _save_image(image: UploadFile, extension: str) -> str:
    filename = uuid4().hex + extension
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / filename
    with open(path, "wb") as buffer:
        buffer.write(image.file.read())
    return f"uploads/{filename}"


@router.post(
    "/items/{item_id}/photo", response_model=ItemRead, status_code=status.HTTP_200_OK
)
def upload_photo(
    item_id: int,
    image: UploadFile,
    repository=Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> ItemRead:
    _get_owned_item(item_id, repository, current_user)
    extension = _validate_image(image)
    photo_path = _save_image(image, extension)
    updated_item = repository.update_item(item_id, {"photo_path": photo_path})
    return _item_to_read(updated_item)
