from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str


class UserOut(UserBase):
    """Schema for outgoing user data responses."""
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str
    role: str


class TokenData(BaseModel):
    """Schema for decoded JWT token payload."""
    email: Optional[str] = None
    role: Optional[str] = None