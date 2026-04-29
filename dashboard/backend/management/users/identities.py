from fastapi import HTTPException

from dashboard.backend.db import is_password_expired
from shared.models import User
from dashboard.backend.models import UserDisplayInformation
from dashboard.backend.db import user_email_free, user_username_free, get_user_permissions_for_project, is_user_administrator, is_user_project_manager, get_user_by_id

async def enforce_availability(email: str, username: str, exclude_user_id: int | None = None) -> None:
    """
    Ensure email and username values are available for use.

    Parameters
    ----------
    email : str
        Email value to validate.
    username : str
        Username value to validate.
    exclude_user_id : int | None, optional
        Optional user identifier to exclude from uniqueness checks.

    Returns
    -------
    None
        None.
    """
    if not await user_email_free(email, exclude_user_id):
        raise HTTPException(status_code=409, detail="Email is already in use.")
    
    if not await user_username_free(username, exclude_user_id):
        raise HTTPException(status_code=409, detail="Username is already in use.")
    
async def convert_orm_to_display_info(user_orm: User, include_role: bool = False, project_id: int | None = None) -> UserDisplayInformation:
    """
    Convert a user ORM entity to a user display DTO.

    Parameters
    ----------
    user_orm : User
        Source user ORM model.
    include_role : bool, optional
        Whether role information should be resolved and included.
    project_id : int | None, optional
        Optional project scope for role resolution.

    Returns
    -------
    UserDisplayInformation
        UserDisplayInformation mapped from ORM data.
    """

    is_admin = False
    try:
        is_admin = await is_user_administrator(user_orm.id)
    except ValueError:
        is_admin = False

    is_project_manager = False
    try:
        if project_id is not None:
            is_project_manager = await is_user_project_manager(user_orm.id, project_id)
    except ValueError:
        is_project_manager = False

    is_expired = False
    try:
        is_expired = await is_password_expired(user_orm.id)
    except ValueError:
        is_expired = False

    role = None
    if include_role:
        role = "User"
        if project_id is not None:
            try:
                permission_record = await get_user_permissions_for_project(project_id, user_orm.id)
            except ValueError:
                permission_record = None
            if permission_record is not None:
                role = permission_record.role.name
        else:
            if is_admin:
                role = "Administrator"
            else:
                try:
                    if await is_user_project_manager(user_orm.id):
                        role = "Project Manager"
                except ValueError:
                    pass

    return UserDisplayInformation(
        id=user_orm.id,
        email=user_orm.email,
        username=user_orm.username,
        profile_picture_url=user_orm.profile_picture_url,
        joined_date=user_orm.joined_date,
        last_login=user_orm.last_login,
        password_expires_at=user_orm.password_expires_at,
        role=role if include_role else None,
        is_admin=is_admin,
        is_project_manager=is_project_manager if project_id is not None else False,
        is_password_expired=is_expired
    )

async def enforce_existing_user(user_id: int) -> User:
    """
    Ensure a user exists and return it.

    Parameters
    ----------
    user_id : int
        Identifier of the user to fetch.

    Returns
    -------
    User
        The found User ORM entity.
    """
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return user