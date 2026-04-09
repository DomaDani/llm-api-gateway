from sqlalchemy import select
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import Project, Status, ProjectPermission

from .users import get_user_by_id
from .roles import get_role_by_name

async def get_project_by_id(project_id: int, session = None) -> Project | None:
    if session is None:
        async with get_session() as session:
            return await get_project_by_id(project_id=project_id, session=session)

    result = await session.execute(select(Project).where(Project.id == project_id))
    return result.scalars().first()

async def get_project_by_name(project_name: str, session = None) -> Project | None:
    if session is None:
        async with get_session() as session:
            return await get_project_by_name(project_name=project_name, session=session)

    result = await session.execute(select(Project).where(Project.name == project_name))
    return result.scalars().first()

async def get_projects_for_user(user_id: int, session = None) -> list[Project]:
    if session is None:
        async with get_session() as session:
            return await get_projects_for_user(user_id=user_id, session=session)

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        return []

    return [permission.project for permission in user.permissions if permission.project.name != "Global"]

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

async def create_project(name: str, manager_id: int, session = None) -> Project:
    if session is None:
        async with get_transactional_session() as session:
            return await create_project(name=name, manager_id=manager_id, session=session)

    project = Project(name=name, status=Status.ACTIVE, created_date=datetime.now(timezone.utc))

    manager_role = await get_role_by_name("Project Manager", session=session)
    if not manager_role:
        raise ValueError("Project Manager role not found.")

    manager_permission = ProjectPermission(project_id=project.id, user_id=manager_id, role_id=manager_role.id, join_date=datetime.now(timezone.utc))

    session.add(project)
    session.add(manager_permission)

    return project

async def delete_project(project_id: int, session = None) -> None:
    if session is None:
        async with get_transactional_session() as session:
            return await delete_project(project_id=project_id, session=session)

    project = await get_project_by_id(project_id=project_id, session=session)
    if project is None:
        raise ValueError("Project not found.")

    await session.delete(project)

