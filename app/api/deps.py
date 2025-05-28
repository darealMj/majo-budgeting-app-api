from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user
from typing import Dict

def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    return current_user
