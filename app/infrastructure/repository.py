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
