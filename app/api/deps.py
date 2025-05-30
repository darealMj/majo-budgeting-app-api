from typing import Dict, Generator, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.connection import get_db

# Security setup (mock implementation for now)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials,
) -> Dict[str, Union[int, str]]:
    """
    Mock authentication dependency.
    TODO: Implement proper JWT validation in future PR.
    """
    # For now, return mock user data
    # In production, this would validate the JWT token and return real user data
    return {"user_id": 1, "email": "user@example.com"}


def get_current_active_user(
    current_user: Dict[str, Union[int, str]]
) -> Dict[str, Union[int, str]]:
    """
    Dependency to get current active user.
    Currently returns mock user data - will be replaced with real JWT implementation.
    """
    # TODO: Add user active/inactive status check when User model is integrated
    # if not current_user.get("is_active", True):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Inactive user"
    #     )
    return current_user


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Ensures proper session cleanup after request.
    """
    return get_db()


CommonDeps = {
    "db": Depends(get_db_session),
    "current_user": Depends(get_current_active_user),
}
