from typing import Dict

from fastapi import APIRouter

# Import endpoint routers (will be added in subsequent PRs)
# from app.api.v1.endpoints import users, accounts, transactions, budgets, analytics

api_router = APIRouter()

# TODO: Include routers as they are implemented in future PRs
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
# api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
# api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
# api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])


@api_router.get("/")
async def api_root() -> Dict[str, str]:
    """
    API root endpoint - provides basic API information.
    """
    return {"message": "Budgeting App API v1", "version": "1.0.0", "status": "active"}
