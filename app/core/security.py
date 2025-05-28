
import jwt
from datetime import datetime
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    # TODO: Implement proper JWT validation
    # For now, return mock user
    return {"user_id": 1, "email": "user@example.com"}

    try:
        # Decode the JWT token
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        
        # Extract user info from token
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        exp: int = payload.get("exp")
        
        # Check if token is expired
        if exp < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
            
        # Verify user exists in database (optional)
        # user = db.query(User).filter(User.id == user_id).first()
        # if not user:
        #     raise HTTPException(status_code=401, detail="User not found")
            
        return {"user_id": user_id, "email": email}
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )