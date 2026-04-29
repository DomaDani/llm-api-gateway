from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import Project, Status, ProjectPermission

from .lookups import get_user_by_id
from .roles import get_role_by_name
from .keys import delete_key
from .quotas import delete_quota

async def get_project_by_id(project_id: int, session = None, options = None, active_only: bool = True) -> Project | None:
    """
    Retrieve a project by identifier.

    Parameters
    ----------
    project_id : int
        Identifier of the project.
    session : optional
        Optional SQLAlchemy session.
    options : optional
        Optional relationship loading options.
    active_only : bool, optional
        Whether to restrict results to active projects.

    Returns
    -------
    Project | None
        The matching Project ORM object, or None.
    """
    if session is None:
        async with get_session() as session:
            return await get_project_by_id(project_id=project_id, session=session, options=options, active_only=active_only)

    status_filter = (Project.status == Status.ACTIVE) if active_only else True
    stmt = select(Project).where(Project.id == project_id, status_filter)
    if options is None:
        options = _get_project_relationship_options()
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    return result.scalars().first()

async def get_project_by_name(project_name: str, session = None, options = None, active_only: bool = True) -> Project | None:
    """
    Retrieve a project by name.

    Parameters
    ----------
    project_name : str
        Name of the project.
    session : optional
        Optional SQLAlchemy session.
    options : optional
        Optional relationship loading options.
    active_only : bool, optional
        Whether to restrict results to active projects.

    Returns
    -------
    Project | None
        The matching Project ORM object, or None.
    """
    if session is None:
        async with get_session() as session:
            return await get_project_by_name(project_name=project_name, session=session, options=options, active_only=active_only)

    status_filter = (Project.status == Status.ACTIVE) if active_only else True
    stmt = select(Project).where(Project.name == project_name, status_filter)
    if options is None:
        options = _get_project_relationship_options()
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    return result.scalars().first()

async def get_projects_for_user(user_id: int, session = None) -> list[Project]:
    """
    Retrieve all active non-global projects assigned to a user.

    Parameters
    ----------
    user_id : int
        Identifier of the user.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    list[Project]
        A list of Project ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_projects_for_user(user_id=user_id, session=session)

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        return []

    return [
        permission.project
        for permission in user.permissions
        if permission.project.name != "Global" and permission.project.status == Status.ACTIVE
    ]

async def create_project(name: str, manager_id: int, session = None) -> Project:
    """
    Create a project and assign its project manager permission.

    Parameters
    ----------
    name : str
        Name for the project.
    manager_id : int
        Identifier of the initial project manager.
    session : optional
        Optional transactional SQLAlchemy session.

    Returns
    -------
    Project
        The created Project ORM object.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await create_project(name=name, manager_id=manager_id, session=session)

    project = Project(name=name, status=Status.ACTIVE, created_date=datetime.now(timezone.utc))
    session.add(project)

    # Ensure the project has a database-generated ID before creating the composite PK permission row.
    await session.flush()

    manager_role = await get_role_by_name("Project Manager", session=session)
    if not manager_role:
        raise ValueError("Project Manager role not found.")

    manager_permission = ProjectPermission(project_id=project.id, user_id=manager_id, role_id=manager_role.id, join_date=datetime.now(timezone.utc))

    session.add(manager_permission)

    return project

async def delete_project(project_id: int, session = None) -> None:
    """
    Archive a project and clean related permissions, keys, and quotas.

    Parameters
    ----------
    project_id : int
        Identifier of the project to archive.
    session : optional
        Optional transactional SQLAlchemy session.

    Returns
    -------
    None
        None.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await delete_project(project_id=project_id, session=session)

    result = await session.execute(
        select(Project).where(Project.id == project_id, Project.status == Status.ACTIVE).with_for_update().options(
            selectinload(Project.permissions),
            selectinload(Project.api_keys),
            selectinload(Project.quotas),
        )
    )
    project = result.scalars().first()
    if project is None:
        raise ValueError("Project not found or already archived.")
    if project.name == "Global":
        raise ValueError("Cannot delete the Global project.")
    
    for permission in project.permissions:
        await session.delete(permission)
    for api_key in project.api_keys:
        if api_key.status == Status.ACTIVE:
            await delete_key(key_id=api_key.id, session=session)
    for quota in project.quotas:
        if quota.key_id is not None:
            continue
        await delete_quota(quota_id=quota.id, session=session)

    project.status = Status.ARCHIVED

async def get_all_projects(session = None) -> list[Project]:
    """
    Retrieve all active projects except the Global project.

    Parameters
    ----------
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    list[Project]
        A list of Project ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_all_projects(session=session)

    result = await session.execute(
        select(Project)
        .where(Project.name != "Global", Project.status == Status.ACTIVE)
        .order_by(Project.name)
    )
    return result.scalars().all()

def _get_project_relationship_options():
    """Return default relationship loading options for project queries."""

    return (
        selectinload(Project.permissions),
        selectinload(Project.api_keys),
        selectinload(Project.quotas),
    )