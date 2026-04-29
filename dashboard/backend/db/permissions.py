from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import Project, User, ProjectPermission, Role

from .projects import get_project_by_id
from .lookups import get_user_by_id
from .roles import get_role_by_name
from .keys import get_keys_for_user, delete_key
from .quotas import delete_quota

async def add_user_to_project(project_id: int, user_id: int, session = None) -> None:
    """
    Add a user to a project with the default user role.

    Parameters
    ----------
    project_id : int
        Identifier of the project.
    user_id : int
        Identifier of the user to add.
    session : optional
        Optional transactional SQLAlchemy session.

    Returns
    -------
    None
        None.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await add_user_to_project(project_id=project_id, user_id=user_id, session=session)

    project = await get_project_by_id(project_id=project_id, session=session)
    if project is None:
        raise ValueError("Project not found.")

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        raise ValueError("User not found.")

    user_role = await get_role_by_name("User", session=session)
    if user_role is None:
        raise ValueError("Default role not found.")

    permission = ProjectPermission(project_id=project.id, user_id=user.id, role_id=user_role.id, join_date=datetime.now(timezone.utc))
    session.add(permission)

async def remove_user_from_project(project_id: int, user_id: int, session = None, users_only: bool = True) -> None:
    """
    Remove a user from a project and clean related project keys and quotas.

    Parameters
    ----------
    project_id : int
        Identifier of the project.
    user_id : int
        Identifier of the user to remove.
    session : optional
        Optional transactional SQLAlchemy session.
    users_only : bool, optional
        Whether project managers are protected from removal.

    Returns
    -------
    None
        None.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await remove_user_from_project(project_id=project_id, user_id=user_id, session=session, users_only=users_only)

    project = await get_project_by_id(project_id=project_id, session=session)
    if project is None:
        raise ValueError("Project not found.")

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        raise ValueError("User not found.")

    permission = await session.execute(
        select(ProjectPermission)
        .where(
            ProjectPermission.project_id == project.id,
            ProjectPermission.user_id == user.id
        )
        .options(
            selectinload(ProjectPermission.role),
            selectinload(ProjectPermission.project),
        )
    )
    permission = permission.scalars().first()

    if permission is None:
        raise ValueError("User does not have permission for this project.")
    if users_only and permission.role.name == "Project Manager":
        raise ValueError("Cannot remove a Project Manager. A Project Manager should only be removed by deleting the project. Set users_only to False to allow removing a Project Manager.")

    user_keys = await get_keys_for_user(user_id=user.id, session=session)
    for key in user_keys:
        if key.project_id == project.id:
            await delete_key(key_id=key.id, session=session)

    for quota in user.quotas:
        if quota.project_id == project.id and quota.key_id is None:
            await delete_quota(quota_id=quota.id, session=session)

    await session.delete(permission)

async def get_user_permissions_for_project(project_id: int, user_id: int, session = None) -> ProjectPermission | None:
    """
    Retrieve a user's permission record for a project.

    Parameters
    ----------
    project_id : int
        Identifier of the project.
    user_id : int
        Identifier of the user.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    ProjectPermission | None
        ProjectPermission ORM object if found, otherwise None.
    """
    if session is None:
        async with get_session() as session:
            return await get_user_permissions_for_project(project_id=project_id, user_id=user_id, session=session)

    project = await get_project_by_id(project_id=project_id, session=session)
    if project is None:
        raise ValueError("Project not found.")

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        raise ValueError("User not found.")

    result = await session.execute(
        select(ProjectPermission)
        .where(
            ProjectPermission.project_id == project.id,
            ProjectPermission.user_id == user.id
        )
        .options(
            selectinload(ProjectPermission.role),
            selectinload(ProjectPermission.project),
        )
    )
    permissions = result.scalars().all()

    if len(permissions) > 1:
        print(f"Warning: User {user_id} has multiple permissions for project {project_id}.")

    return permissions[0] if permissions else None

async def is_user_project_member(project_id: int, user_id: int, session = None) -> bool:
    """
    Check whether a user is a member of a project.

    Parameters
    ----------
    project_id : int
        Identifier of the project.
    user_id : int
        Identifier of the user.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    bool
        True if membership exists, otherwise False.
    """
    if session is None:
        async with get_session() as session:
            return await is_user_project_member(project_id=project_id, user_id=user_id, session=session)

    permission = await get_user_permissions_for_project(project_id=project_id, user_id=user_id, session=session)
    return permission is not None

async def is_user_project_manager(user_id: int, project_id: int | None = None, session = None) -> bool:
    """
    Check whether a user has project manager role.

    Parameters
    ----------
    user_id : int
        Identifier of the user.
    project_id : int | None, optional
        Optional project identifier for project-scoped check.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    bool
        True if the user is a project manager in the requested scope.
    """
    if session is None:
        async with get_session() as session:
            return await is_user_project_manager(project_id=project_id, user_id=user_id, session=session)

    if project_id is not None:
        permission = await get_user_permissions_for_project(project_id=project_id, user_id=user_id, session=session)
        return permission is not None and permission.role.name == "Project Manager"
    else:
        user = await get_user_by_id(user_id=user_id, session=session)
        if user is None:
            raise ValueError("User not found.")

        for permission in user.permissions:
            if permission.role.name == "Project Manager":
                return True

        return False

async def is_user_administrator(user_id: int, session = None) -> bool:
    """
    Check whether a user has global administrator role.

    Parameters
    ----------
    user_id : int
        Identifier of the user.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    bool
        True if the user is a global administrator, otherwise False.
    """
    if session is None:
        async with get_session() as session:
            return await is_user_administrator(user_id=user_id, session=session)

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        raise ValueError("User not found.")

    for permission in user.permissions:
        if permission.project.name == "Global" and permission.role.name == "Administrator":
            return True

    return False