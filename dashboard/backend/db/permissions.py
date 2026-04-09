from sqlalchemy import select
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import Project, User, ProjectPermission, Role

from .projects import get_project_by_id
from .users import get_user_by_id
from .roles import get_role_by_name

async def add_user_to_project(project_id: int, user_id: int, session = None) -> None:
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
        select(ProjectPermission).where(
            ProjectPermission.project_id == project.id,
            ProjectPermission.user_id == user.id
        )
    )
    permission = permission.scalars().first()

    if permission is None:
        raise ValueError("User does not have permission for this project.")
    if users_only and permission.role.name == "Project Manager":
        raise ValueError("Cannot remove a Project Manager. A Project Manager should only be removed by deleting the project. Set users_only to False to allow removing a Project Manager.")

    await session.delete(permission)

async def get_user_permissions_for_project(project_id: int, user_id: int, session = None) -> ProjectPermission | None:
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
        select(ProjectPermission).where(
            ProjectPermission.project_id == project.id,
            ProjectPermission.user_id == user.id
        )
    )
    permissions = result.scalars().all()

    if len(permissions) > 1:
        print(f"Warning: User {user_id} has multiple permissions for project {project_id}.")

    return permissions[0] if permissions else None

async def is_user_project_member(project_id: int, user_id: int, session = None) -> bool:
    if session is None:
        async with get_session() as session:
            return await is_user_project_member(project_id=project_id, user_id=user_id, session=session)

    permission = await get_user_permissions_for_project(project_id=project_id, user_id=user_id, session=session)
    return permission is not None

async def is_user_project_manager(project_id: int, user_id: int, session = None) -> bool:
    if session is None:
        async with get_session() as session:
            return await is_user_project_manager(project_id=project_id, user_id=user_id, session=session)

    permission = await get_user_permissions_for_project(project_id=project_id, user_id=user_id, session=session)
    return permission is not None and permission.role.name == "Project Manager"

async def is_user_administrator(user_id: int, session = None) -> bool:
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