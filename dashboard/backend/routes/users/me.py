from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from dashboard.backend.models import UserDisplayInformation
from dashboard.backend.auth import get_user_from_token

router = APIRouter(prefix="/users", tags=["users"])

_bearer = HTTPBearer()

@router.get("/me", response_model=UserDisplayInformation, description="Get current authenticated user's information")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer), project_id: Optional[int] = None) -> UserDisplayInformation:
    """
    Return the current authenticated user's profile information.

    Parameters
    ----------
    - credentials: Bearer authorization credentials containing the access token.
    - project_id: Optional project context used when resolving role-specific fields.

    Returns
    -------
    - UserDisplayInformation for the token subject.
    """
    user = await get_user_from_token(credentials.credentials, project_id=project_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user