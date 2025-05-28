from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from app.api.deps import get_current_active_user
from app.database.connection import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse

router = APIRouter()

@router.post("/", response_model=AccountResponse)
async def create_account(
    account: AccountCreate, 
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    db_account = Account(**account.dict(), user_id=current_user["user_id"])
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=List[AccountResponse])
async def get_accounts(
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    accounts = db.query(Account).filter(Account.user_id == current_user["user_id"]).all()
    return accounts