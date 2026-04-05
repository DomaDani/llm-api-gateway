from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from dashboard.backend.models import UserDisplayInfo
from dashboard.backend.auth import get_user_from_token

router = APIRouter(prefix="/users", tags=["users"])

_bearer = HTTPBearer()

@router.get("/me", response_model=UserDisplayInfo, description="Get current authenticated user's information")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> UserDisplayInfo:
    user = await get_user_from_token(credentials.credentials)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user