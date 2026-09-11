from datetime import date

from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user, get_repository
from app.domain.exceptions import ItemNotFound
from app.domain.inventory import Item
from app.domain.user import User
from app.schemas import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()


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
    return items_for_return


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
