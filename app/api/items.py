from datetime import date

from fastapi import APIRouter, Depends, status

from app.dependencies import get_repository
from app.domain.inventory import Item
from app.schemas import ItemCreate, ItemRead


router = APIRouter()


@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, repository=Depends(get_repository)) -> Item:
    item_created = Item(
        name=item.name,
        quantity=item.quantity,
        expiry_date=item.expiry_date,
        user_id=1,
        added_date=date.today()
    )
    new_item = repository.add_item(item_created)
    return new_item