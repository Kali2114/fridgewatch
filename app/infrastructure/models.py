from sqlalchemy import Boolean, Column, Date, Integer, String

from app.infrastructure.database import Base


class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String)
    quantity = Column(Integer)
    added_date = Column(Date)
    expiry_date = Column(Date)


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean)
