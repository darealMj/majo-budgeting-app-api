from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.schemas.transaction import CategoryType


class BudgetPeriod(str, Enum):
    """Budget period types"""

    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class BudgetStatus(str, Enum):
    """Budget status types"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    EXCEEDED = "exceeded"


class BudgetBase(BaseModel):
    """Base budget schema with common fields"""

    name: str = Field(..., min_length=1, max_length=100, description="Budget name")
    category: CategoryType = Field(..., description="Budget category")
    amount: float = Field(..., gt=0, description="Budget amount (must be positive)")
    period: BudgetPeriod = Field(BudgetPeriod.MONTHLY, description="Budget period")


class BudgetCreate(BudgetBase):
    """Schema for creating a new budget"""

    start_date: Optional[datetime] = Field(
        None, description="Budget start date (defaults to beginning of current month)"
    )
    end_date: Optional[datetime] = Field(
        None, description="Budget end date (calculated based on period if not provided)"
    )

    @validator("start_date", pre=True, always=True)
    def set_start_date(cls, v: Optional[datetime]) -> datetime:
        """Set start date to beginning of current month if not provided"""
        if v is None:
            now = datetime.utcnow()
            return datetime(now.year, now.month, 1)
        return v

    @validator("end_date", pre=True, always=True)
    def calculate_end_date(
        cls, v: Optional[datetime], values: dict
    ) -> Optional[datetime]:
        """Calculate end date based on period if not provided"""
        if v is not None:
            return v

        start_date: Optional[datetime] = values.get("start_date")
        period: Optional[BudgetPeriod] = values.get("period")

        if start_date is not None and period is not None:
            if period == BudgetPeriod.WEEKLY:
                return start_date + timedelta(weeks=1)
            elif period == BudgetPeriod.MONTHLY:
                if start_date.month == 12:
                    return datetime(start_date.year + 1, 1, 1) - timedelta(days=1)
                else:
                    return datetime(
                        start_date.year, start_date.month + 1, 1
                    ) - timedelta(days=1)
            elif period == BudgetPeriod.QUARTERLY:
                month = start_date.month
                quarter_end_month = ((month - 1) // 3 + 1) * 3
                if quarter_end_month == 12:
                    return datetime(start_date.year + 1, 1, 1) - timedelta(days=1)
                else:
                    return datetime(
                        start_date.year, quarter_end_month + 1, 1
                    ) - timedelta(days=1)
            elif period == BudgetPeriod.YEARLY:
                return datetime(start_date.year + 1, 1, 1) - timedelta(days=1)

        return None

    @validator("category")
    def validate_expense_category(cls, v: CategoryType) -> CategoryType:
        """Ensure budget category is appropriate for expenses"""
        income_categories = {
            CategoryType.SALARY,
            CategoryType.FREELANCE,
            CategoryType.INVESTMENT,
            CategoryType.BONUS,
        }
        if v in income_categories:
            raise ValueError(f"Cannot create budget for income category '{v}'")
        return v


class BudgetUpdate(BaseModel):
    """Schema for updating budget information"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    period: Optional[BudgetPeriod] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class BudgetResponse(BudgetBase):
    """Schema for budget API responses"""

    id: int
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BudgetAnalysis(BaseModel):
    """Schema for budget analysis data"""

    budget_id: int
    budget_name: str
    category: str
    budgeted_amount: float
    actual_spent: float
    remaining: float
    percentage_used: float
    status: BudgetStatus
    days_remaining: Optional[int]

    @validator("status", pre=True, always=True)
    def determine_status(cls, v: Optional[BudgetStatus], values: dict) -> BudgetStatus:
        """Automatically determine budget status based on spending"""
        if v is not None:
            return v

        percentage_used = values.get("percentage_used", 0)
        remaining = values.get("remaining", 0)

        if percentage_used >= 100:
            return BudgetStatus.EXCEEDED
        elif remaining <= 0:
            return BudgetStatus.COMPLETED
        else:
            return BudgetStatus.ACTIVE


class BudgetSummary(BaseModel):
    """Schema for overall budget summary"""

    total_budgets: int
    active_budgets: int
    total_budgeted: float
    total_spent: float
    total_remaining: float
    budgets_exceeded: int
    overall_percentage_used: float
