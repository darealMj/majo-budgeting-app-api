from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: str
    name: str


class UserCreate(UserBase):
    """Schema for creating a new user."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    email: Optional[str] = None
    name: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user API responses."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
