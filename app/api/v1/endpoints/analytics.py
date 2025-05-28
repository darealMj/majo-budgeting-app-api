from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict
from datetime import date

from app.api.deps import get_current_active_user
from app.database.connection import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.schemas.transaction import TransactionType

router = APIRouter()

@router.get("/spending-by-category")
async def get_spending_by_category(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).join(Account).filter(
        Account.user_id == current_user["user_id"],
        Transaction.transaction_type == TransactionType.EXPENSE
    )
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.all()
    
    spending = {}
    for t in transactions:
        category = t.category
        spending[category] = spending.get(category, 0) + abs(t.amount)
    
    return {"spending_by_category": spending}

@router.get("/budget-vs-actual")
async def get_budget_vs_actual(
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    budgets = db.query(Budget).filter(
        Budget.user_id == current_user["user_id"],
        Budget.is_active == True
    ).all()
    
    result = []
    for budget in budgets:
        actual_spending = db.query(Transaction).join(Account).filter(
            Account.user_id == current_user["user_id"],
            Transaction.category == budget.category,
            Transaction.transaction_type == TransactionType.EXPENSE,
            Transaction.date >= budget.start_date
        ).all()
        
        total_spent = sum(abs(t.amount) for t in actual_spending)
        
        result.append({
            "budget_name": budget.name,
            "category": budget.category,
            "budgeted_amount": budget.amount,
            "actual_spent": total_spent,
            "remaining": budget.amount - total_spent,
            "percentage_used": (total_spent / budget.amount * 100) if budget.amount > 0 else 0
        })
    
    return {"budget_analysis": result}
