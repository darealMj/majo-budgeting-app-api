from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


class TransactionType(str, Enum):
    """Transaction type classifications."""

    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class CategoryType(str, Enum):
    """Transaction categories."""

    # Housing
    HOUSING = "housing"
    RENT_MORTGAGE = "rent_mortgage"
    UTILITIES = "utilities"

    # Transportation
    TRANSPORTATION = "transportation"
    GAS = "gas"
    PUBLIC_TRANSPORT = "public_transport"
    CAR_MAINTENANCE = "car_maintenance"

    # Food
    FOOD = "food"
    GROCERIES = "groceries"
    RESTAURANTS = "restaurants"

    # Entertainment
    ENTERTAINMENT = "entertainment"
    MOVIES = "movies"
    SUBSCRIPTIONS = "subscriptions"

    # Health
    HEALTHCARE = "healthcare"
    MEDICAL = "medical"
    PHARMACY = "pharmacy"

    # Shopping
    SHOPPING = "shopping"
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"

    # Education
    EDUCATION = "education"
    BOOKS = "books"
    COURSES = "courses"

    # Income
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    BONUS = "bonus"

    # Other
    OTHER = "other"
    TRANSFER = "transfer"


class TransactionBase(BaseModel):
    """Base transaction schema with common fields."""

    amount: float = Field(..., description="Transaction amount")
    description: str = Field(
        ..., min_length=1, max_length=255, description="Transaction description"
    )
    category: CategoryType = Field(..., description="Transaction category")
    transaction_type: TransactionType = Field(..., description="Type of transaction")


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""

    account_id: int = Field(..., description="ID of the associated account")
    date: Optional[datetime] = Field(
        None, description="Transaction date (defaults to now)"
    )

    @field_validator("date")
    @classmethod
    def set_date(cls, v: Optional[datetime]) -> datetime:
        """Set transaction date to now if not provided."""
        return v or datetime.utcnow()

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float, info: ValidationInfo) -> float:
        """Ensure expense amounts are negative and income amounts are
        positive."""
        # Access other field values through info.data
        values = info.data if info.data else {}
        if "transaction_type" in values:
            if values["transaction_type"] == TransactionType.EXPENSE:
                return -abs(v)  # Ensure expenses are negative
            elif values["transaction_type"] == TransactionType.INCOME:
                return abs(v)  # Ensure income is positive
        return v

    @field_validator("category")
    @classmethod
    def validate_category_type_match(
        cls, v: CategoryType, info: ValidationInfo
    ) -> CategoryType:
        """Validate that category matches transaction type."""
        # Access other field values through info.data
        values = info.data if info.data else {}
        if "transaction_type" in values:
            income_categories = {
                CategoryType.SALARY,
                CategoryType.FREELANCE,
                CategoryType.INVESTMENT,
                CategoryType.BONUS,
            }

            if values["transaction_type"] == TransactionType.INCOME:
                if v not in income_categories:
                    raise ValueError(
                        f"Category '{v}' is not valid for income transactions"
                    )
            elif values["transaction_type"] == TransactionType.EXPENSE:
                if v in income_categories:
                    raise ValueError(
                        f"Category '{v}' is not valid for expense transactions"
                    )
        return v


class TransactionUpdate(BaseModel):
    """Schema for updating transaction information."""

    amount: Optional[float] = None
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[CategoryType] = None
    transaction_type: Optional[TransactionType] = None
    date: Optional[datetime] = None


class TransactionResponse(TransactionBase):
    """Schema for transaction API responses."""

    id: int
    account_id: int
    date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionSummary(BaseModel):
    """Schema for transaction summary data."""

    total_income: float
    total_expenses: float
    net_amount: float
    transaction_count: int
