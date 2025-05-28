from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class CategoryType(str, Enum):
    HOUSING = "housing"
    FOOD = "food"
    TRANSPORTATION = "transportation"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    EDUCATION = "education"
    OTHER = "other"

class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    description: str
    category: CategoryType
    transaction_type: TransactionType
    date: Optional[datetime] = None
    
    @validator('date', pre=True, always=True)
    def set_date(cls, v):
        return v or datetime.utcnow()
    
    @validator('amount')
    def validate_amount(cls, v, values):
        if 'transaction_type' in values and values['transaction_type'] == TransactionType.EXPENSE:
            return -abs(v)
        return abs(v) if values.get('transaction_type') == TransactionType.INCOME else v

class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    category: str
    transaction_type: str
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True