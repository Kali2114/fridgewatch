from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    expiry_date: date


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    quantity: int
    expiry_date: date
    added_date: date
    user_id: int


class ItemUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = Field(default=None, gt=0)
    expiry_date: date | None = None
