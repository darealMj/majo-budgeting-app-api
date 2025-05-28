from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccountCreate(BaseModel):
    name: str
    account_type: str
    balance: Optional[float] = 0.0

class AccountResponse(BaseModel):
    id: int
    name: str
    account_type: str
    balance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
