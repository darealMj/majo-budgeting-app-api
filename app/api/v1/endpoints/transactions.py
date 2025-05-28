from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict

from app.api.deps import get_current_active_user
from app.database.connection import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate, 
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.id == transaction.account_id, 
        Account.user_id == current_user["user_id"]
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    
    account.balance += transaction.amount
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    account_id: Optional[int] = None,
    limit: int = 50,
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).join(Account).filter(Account.user_id == current_user["user_id"])
    
    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    
    transactions = query.order_by(Transaction.date.desc()).limit(limit).all()
    return transactions