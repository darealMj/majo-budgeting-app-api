from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

from app.models.account import Account
from app.models.budget import Budget
from app.models.transaction import Transaction

# Import all models to ensure they are registered
from app.models.user import User


class Base(DeclarativeBase):
    pass
