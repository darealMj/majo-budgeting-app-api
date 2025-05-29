from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AccountType(str, Enum):
    """Supported account types"""

    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    CASH = "cash"
    OTHER = "other"


class AccountBase(BaseModel):
    """Base account schema with common fields"""

    name: str = Field(..., min_length=1, max_length=100, description="Account name")
    account_type: AccountType = Field(..., description="Type of financial account")


class AccountCreate(AccountBase):
    """Schema for creating a new account"""

    balance: Optional[float] = Field(0.0, description="Initial account balance")


class AccountUpdate(BaseModel):
    """Schema for updating account information"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    account_type: Optional[AccountType] = None
    is_active: Optional[bool] = None


class AccountResponse(AccountBase):
    """Schema for account API responses"""

    id: int
    balance: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
