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
        return self._to_domain(model)

    def list_for_user(self, user_id):
        statement = select(ItemModel).where(ItemModel.user_id == user_id)
        result = self.session.execute(statement)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    def delete_item(self, item_id):
        model = self.session.get(ItemModel, item_id)
        if model is None:
            raise ItemNotFound(f"Item {item_id} not found")
        self.session.delete(model)
        self.session.commit()

    def update_item(self, item_id, payload):
        model = self.session.get(ItemModel, item_id)
        if model is None:
            raise ItemNotFound(f"Item {item_id} not found")

        domain_item = self._to_domain(model)
        for key, value in payload.items():
            setattr(domain_item, key, value)

        model.name = domain_item.name
        model.quantity = domain_item.quantity
        model.added_date = domain_item.added_date
        model.expiry_date = domain_item.expiry_date
        self.session.commit()
        return domain_item

    @staticmethod
    def _to_domain(model):
        return Item(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            quantity=model.quantity,
            added_date=model.added_date,
            expiry_date=model.expiry_date,
        )
