from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from dashboard.backend.models import UserDisplayInformation
from dashboard.backend.auth import get_user_from_token

router = APIRouter(prefix="/users", tags=["users"])

_bearer = HTTPBearer()

@router.get("/me", response_model=UserDisplayInformation, description="Get current authenticated user's information")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer), project_id: Optional[int] = None) -> UserDisplayInformation:
    user = await get_user_from_token(credentials.credentials, project_id=project_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user