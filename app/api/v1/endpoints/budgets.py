from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime

from app.api.deps import get_current_active_user
from app.database.connection import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetResponse

router = APIRouter()

@router.post("/", response_model=BudgetResponse)
async def create_budget(
    budget: BudgetCreate, 
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    budget_data = budget.dict()
    if not budget_data.get('start_date'):
        budget_data['start_date'] = datetime.utcnow().replace(day=1)
    
    db_budget = Budget(**budget_data, user_id=current_user["user_id"])
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    current_user: Dict = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    budgets = db.query(Budget).filter(Budget.user_id == current_user["user_id"]).all()
    return budgets
