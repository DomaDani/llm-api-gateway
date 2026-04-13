from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserDisplayInformation
from dashboard.backend.db import get_all_users as db_get_all_users
from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import user_convert_orm_to_display_info as convert_orm_to_display_info

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/everyone", response_model=list[UserDisplayInformation], description="Get information about all users")
async def get_all_users(_: None = Depends(require_valid_access_token)) -> list[UserDisplayInformation]:
    try:
        user_orms = await db_get_all_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching users. Please try again later.") from e

    return [await convert_orm_to_display_info(user_orm) for user_orm in user_orms]