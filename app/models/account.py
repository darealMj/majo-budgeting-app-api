from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    account_type = Column(String)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
