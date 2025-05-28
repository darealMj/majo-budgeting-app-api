from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True