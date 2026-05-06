from pydantic import BaseModel, EmailStr
from typing import Optional

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.EMPLOYEE


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None