from sqlalchemy import Column, Date, Integer, String

from app.infrastructure.database import Base


class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String)
    quantity = Column(Integer)
    added_date = Column(Date)
    expiry_date = Column(Date)
