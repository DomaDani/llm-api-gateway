from fastapi import HTTPException

from shared.models import User
from dashboard.backend.models import UserDisplayInfo
from dashboard.backend.db import user_email_free, user_username_free

async def enforce_availability(email: str, username: str, exclude_user_id: int | None = None) -> None:
    if not await user_email_free(email, exclude_user_id):
        raise HTTPException(status_code=409, detail="Email is already in use.")
    
    if not await user_username_free(username, exclude_user_id):
        raise HTTPException(status_code=409, detail="Username is already in use.")
    
async def convert_orm_to_display_info(user_orm: User) -> UserDisplayInfo:
    return UserDisplayInfo(
        id=user_orm.id,
        email=user_orm.email,
        username=user_orm.username,
        profile_picture_url=user_orm.profile_picture_url,
        joined_date=user_orm.joined_date,
        last_login=user_orm.last_login,
        password_expires_at=user_orm.password_expires_at
    )