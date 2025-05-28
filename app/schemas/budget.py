from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.transaction import CategoryType

class BudgetCreate(BaseModel):
    name: str
    category: CategoryType
    amount: float
    period: str = "monthly"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class BudgetResponse(BaseModel):
    id: int
    name: str
    category: str
    amount: float
    period: str
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
