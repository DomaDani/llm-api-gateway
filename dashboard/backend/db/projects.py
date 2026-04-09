from sqlalchemy import select
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import Project, Status, ProjectPermission

from .lookups import get_user_by_id
from .roles import get_role_by_name
from .keys import delete_key
from .quotas import delete_quota

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

    result = await session.execute(select(Project).where(Project.id == project_id).with_for_update())
    project = result.scalars().first()
    if project is None:
        raise ValueError("Project not found.")
    if project.name == "Global":
        raise ValueError("Cannot delete the Global project.")
    
    for permission in project.permissions:
        await session.delete(permission)
    for api_key in project.api_keys:
        await delete_key(key_id=api_key.id, session=session)
    for quota in project.quotas:
        await delete_quota(quota_id=quota.id, session=session)

    await session.delete(project)

async def get_all_projects(session = None) -> list[Project]:
    if session is None:
        async with get_session() as session:
            return await get_all_projects(session=session)

    result = await session.execute(select(Project).order_by(Project.name))
    return result.scalars().all()
