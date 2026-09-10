from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    is_active: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
