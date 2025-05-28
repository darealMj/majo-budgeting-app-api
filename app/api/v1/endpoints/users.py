from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from app.api.deps import get_current_active_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
