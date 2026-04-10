from fastapi import HTTPException

from shared.models import User
from dashboard.backend.models import UserDisplayInformation
from dashboard.backend.db import user_email_free, user_username_free, get_user_permissions_for_project, is_user_administrator, is_user_project_manager, get_user_by_id

async def enforce_availability(email: str, username: str, exclude_user_id: int | None = None) -> None:
    if not await user_email_free(email, exclude_user_id):
        raise HTTPException(status_code=409, detail="Email is already in use.")
    
    if not await user_username_free(username, exclude_user_id):
        raise HTTPException(status_code=409, detail="Username is already in use.")
    
async def convert_orm_to_display_info(user_orm: User, include_role: bool = False, project_id: int | None = None) -> UserDisplayInformation:

    if include_role:
        if project_id is not None:
            permission_record = await get_user_permissions_for_project(user_orm.id, project_id)
            if permission_record is not None:
                role = permission_record.role.name
        else:
            if await is_user_administrator(user_orm.id):
                role = "Administrator"
            elif await is_user_project_manager(user_orm.id):
                role = "Project Manager"
            else:
                role = "User"

    return UserDisplayInformation(
        id=user_orm.id,
        email=user_orm.email,
        username=user_orm.username,
        profile_picture_url=user_orm.profile_picture_url,
        joined_date=user_orm.joined_date,
        last_login=user_orm.last_login,
        password_expires_at=user_orm.password_expires_at,
        role=role if include_role else None
    )

async def enforce_existing_user(user_id: int) -> User:
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return user