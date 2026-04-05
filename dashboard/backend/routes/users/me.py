from fastapi import APIRouter, Depends

from backend.models import UserDisplayInfo
from backend.auth import get_user_from_token

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserDisplayInfo, description="Get current authenticated user's information")
async def get_current_user(current_user: dict = Depends(get_user_from_token)) -> UserDisplayInfo:
    return current_user