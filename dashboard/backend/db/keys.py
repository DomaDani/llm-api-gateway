from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import APIKey, Project, User, Status

async def get_key_by_id(
    key_id: int,
    session = None,
    options = None,
    active_only: bool = True,
) -> APIKey | None:
    """
    Retrieve an API key by identifier.
    If a session is provided, it uses that session; otherwise, it creates a new session for the query.

    Parameters
    ----------
    - key_id: Identifier of the API key.
    - session: Optional SQLAlchemy session.
    - options: Optional relationship loading options.
    - active_only: Whether to restrict results to active keys and active projects.

    Returns
    -------
    - The matching APIKey ORM object, or None if not found.
    """
    if session is None:
        async with get_session() as session:
            return await get_key_by_id(key_id=key_id, session=session, options=options, active_only=active_only)

    status_filter = (APIKey.status == Status.ACTIVE) if active_only else True
    stmt = (
        select(APIKey)
        .join(Project, APIKey.project_id == Project.id)
        .where(and_(APIKey.id == key_id, status_filter, Project.status == Status.ACTIVE))
    )
    if options is None:
        options = get_key_relationship_options()
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    return result.scalars().first()

async def get_keys_for_user(user_id: int, project_id = None, session = None, active_only: bool = True) -> list[APIKey]:
    """
    Retrieve all API keys belonging to a user, or the user's keys in a project if a project is provided.
    If a session is provided, it uses that session; otherwise, it creates a new session for the query.

    Parameters
    ----------
    - user_id: Identifier of the user.
    - session: Optional SQLAlchemy session.
    - active_only: Whether to restrict results to active keys and active projects.

    Returns
    -------
    - A list of APIKey ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_keys_for_user(user_id=user_id, project_id=project_id, session=session, active_only=active_only)

    status_filter = (APIKey.status == Status.ACTIVE) if active_only else True

    result = await session.execute(
        select(APIKey)
        .join(Project, APIKey.project_id == Project.id)
        .where(and_(APIKey.user_id == user_id, status_filter, Project.status == Status.ACTIVE, True if project_id is None else APIKey.project_id == project_id))
        .options(selectinload(APIKey.user))
    )
    return result.scalars().all()

async def get_keys_for_project(project_id: int, session = None, active_only: bool = True) -> list[APIKey]:
    """
    Retrieve all API keys for a project.

    Parameters
    ----------
    - project_id: Identifier of the project.
    - session: Optional SQLAlchemy session.
    - active_only: Whether to restrict results to active keys and active projects.

    Returns
    -------
    - A list of APIKey ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_keys_for_project(project_id=project_id, session=session, active_only=active_only)

    status_filter = (APIKey.status == Status.ACTIVE) if active_only else True

    result = await session.execute(
        select(APIKey)
        .join(Project, APIKey.project_id == Project.id)
        .where(and_(APIKey.project_id == project_id, status_filter, Project.status == Status.ACTIVE))
        .options(selectinload(APIKey.user))
    )
    return result.scalars().all()

async def get_all_keys(session = None, active_only: bool = True) -> list[APIKey]:
    """
    Retrieve all API keys across projects.

    Parameters
    ----------
    - session: Optional SQLAlchemy session.
    - active_only: Whether to restrict results to active keys and active projects.

    Returns
    -------
    - A list of APIKey ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_all_keys(session=session, active_only=active_only)

    status_filter = (APIKey.status == Status.ACTIVE) if active_only else True
    result = await session.execute(
        select(APIKey)
        .join(Project, APIKey.project_id == Project.id)
        .where(and_(status_filter, Project.status == Status.ACTIVE))
        .order_by(APIKey.name)
    )
    return result.scalars().all()

async def create_key(
        project_id: int,
        user_id: int,
        name: str,
        fingerprint: str,
        key_hash: str,
        session = None
) -> APIKey:
    """
    Create a new API key record in the database.

    Parameters
    ----------
    - project_id: Project identifier for the key.
    - user_id: Owner user identifier.
    - name: Human-readable key name.
    - fingerprint: Key fingerprint value.
    - key_hash: Hashed key value.
    - session: Optional transactional SQLAlchemy session.

    Returns
    -------
    - The created APIKey ORM object.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await create_key(
                project_id=project_id,
                user_id=user_id,
                name=name,
                fingerprint=fingerprint,
                key_hash=key_hash,
                session=session
            )
        
    key = APIKey(
        project_id=project_id,
        user_id=user_id,
        name=name,
        fingerprint=fingerprint,
        key_hash=key_hash,
        create_date=datetime.now(timezone.utc),
        status=Status.ACTIVE
    )

    session.add(key)

    return key

async def delete_key(key_id: int, session = None) -> None:
    """
    Archive an API key and delete quotas targeting it.

    Parameters
    ----------
    - key_id: Identifier of the API key to archive.
    - session: Optional transactional SQLAlchemy session.

    Returns
    -------
    - None.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await delete_key(key_id=key_id, session=session)

    result = await session.execute(
        select(APIKey)
        .where(and_(APIKey.id == key_id, APIKey.status == Status.ACTIVE))
        .options(selectinload(APIKey.quotas))
        .with_for_update()
    )
    key = result.scalars().first()
    if key is None:
        raise ValueError("API Key not found or already archived.")
    
    for quota in key.quotas:
        await session.delete(quota)

    key.status = Status.ARCHIVED

async def get_key_ownership(key_id: int, session = None) -> tuple[Project, User]:
    """
    Retrieve the project and user owning an API key.

    Parameters
    ----------
    - key_id: Identifier of the API key.
    - session: Optional SQLAlchemy session.

    Returns
    -------
    - A tuple of project and user ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_key_ownership(key_id=key_id, session=session)

    result = await session.execute(
        select(APIKey)
        .join(Project, APIKey.project_id == Project.id)
        .where(
            APIKey.id == key_id,
            APIKey.status == Status.ACTIVE,
            Project.status == Status.ACTIVE,
        )
        .options(
            selectinload(APIKey.project),
            selectinload(APIKey.user),
        )
    )

    key = result.scalars().first()

    if key is None:
        raise ValueError("API Key not found or not active.")
    
    return (key.project, key.user)

def get_key_relationship_options():
    """Return default relationship loading options for API key queries."""

    return (
        selectinload(APIKey.quotas),
        selectinload(APIKey.project),
        selectinload(APIKey.user),
    )