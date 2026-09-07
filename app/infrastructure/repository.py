from sqlalchemy import select

from app.domain.exceptions import ItemNotFound
from app.domain.inventory import Item
from app.infrastructure.models import ItemModel


class SQLAlchemyItemRepository:
    def __init__(self, session):
        self.session = session

    def add_item(self, item):
        model = ItemModel(
            user_id=item.user_id,
            name=item.name,
            quantity=item.quantity,
            added_date=item.added_date,
            expiry_date=item.expiry_date,
        )
        self.session.add(model)
        self.session.commit()
        item.id = model.id
        return item

    def get_item(self, item_id):
        model = self.session.get(ItemModel, item_id)
        if model is None:
            raise ItemNotFound(f"Item {item_id} not found")
        return Item(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            quantity=model.quantity,
            added_date=model.added_date,
            expiry_date=model.expiry_date,
        )

    def list_for_user(self, user_id):
        statement = select(ItemModel).where(ItemModel.user_id == user_id)
        result = self.session.execute(statement)
        result = result.scalars().all()
        results = []
        for model in result:
            item = Item(
                id=model.id,
                user_id=model.user_id,
                name=model.name,
                quantity=model.quantity,
                added_date=model.added_date,
                expiry_date=model.expiry_date,
            )
            results.append(item)
        return results
