from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models to ensure they are registered
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.budget import Budget
