from fastapi import APIRouter, Depends

from dashboard.backend.models import UserDisplayInfo
from dashboard.backend.db import get_all_users
from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import user_convert_orm_to_display_info as convert_orm_to_display_info

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/everyone", response_model=list[UserDisplayInfo], description="Get information about all users")
async def get_all_users(_: None = Depends(require_valid_access_token)) -> list[UserDisplayInfo]:
    user_orms = await get_all_users()
    return [await convert_orm_to_display_info(user_orm) for user_orm in user_orms]