from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import Quota, Status, Period, User, Project, APIKey
from shared.utils import calculate_date_after_period

from .lookups import get_user_by_id

async def get_quota_by_id(quota_id: int, session = None, options = None) -> Quota | None:
    """
    Retrieve a quota by identifier.

    Parameters
    ----------
    - quota_id: Identifier of the quota.
    - session: Optional SQLAlchemy session.
    - options: Optional relationship loading options.

    Returns
    -------
    - The matching Quota ORM object, or None.
    """
    if session is None:
        async with get_session() as session:
            return await get_quota_by_id(quota_id=quota_id, session=session, options=options)

    stmt = select(Quota).where(Quota.id == quota_id)
    if options is None:
        options = _get_quotas_relationship_options()
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    return result.scalars().first()

async def get_global_quotas(
        session = None,
        include_targeted: bool = False,
    active_only: bool = False,
    options = None
) -> list[Quota]:
    """
    Retrieve global quotas, optionally including targeted variants.

    Parameters
    ----------
    - session: Optional SQLAlchemy session.
    - include_targeted: Whether targeted global quotas are included.
    - active_only: Whether to restrict results to active quotas.
    - options: Optional relationship loading options.

    Returns
    -------
    - A list of Quota ORM objects.
    """

    if session is None:
        async with get_session() as session:
            return await get_global_quotas(
                session=session,
                include_targeted=include_targeted,
                active_only=active_only,
                options=options
            )

    active_filter = (Quota.status == Status.ACTIVE) if active_only else True
    if options is None:
        options = _get_quotas_relationship_options()
    

    if include_targeted:
        stmt = select(Quota).where(
            and_(
                Quota.project_id.is_(None),
                active_filter
            )
        )
    else:
        stmt = select(Quota).where(
            and_(
                Quota.user_id.is_(None),
                Quota.project_id.is_(None),
                Quota.key_id.is_(None),
                active_filter
            )
        )

    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    
    return result.scalars().all()

async def get_quotas_for_project(
        project_id: int,
        session = None,
        include_targeted: bool = False,
        include_inherited: bool = True,
    active_only: bool = False,
    options = None
) -> list[Quota]:
    """
    Retrieve quotas for a project with optional inherited global quotas.

    Parameters
    ----------
    - project_id: Identifier of the project.
    - session: Optional SQLAlchemy session.
    - include_targeted: Whether targeted project quotas are included.
    - include_inherited: Whether global quotas are appended.
    - active_only: Whether to restrict results to active quotas.
    - options: Optional relationship loading options.

    Returns
    -------
    - A list of Quota ORM objects.
    """
    
    if session is None:
        async with get_session() as session:
            return await get_quotas_for_project(
                project_id=project_id,
                session=session,
                include_targeted=include_targeted,
                include_inherited=include_inherited,
                active_only=active_only,
                options=options
            )

    active_filter = (Quota.status == Status.ACTIVE) if active_only else True
    if options is None:
        options = _get_quotas_relationship_options()

    if include_targeted:
        stmt = select(Quota).where(
            and_(
                or_(
                    Quota.project_id == project_id,
                    and_(
                        Quota.project_id.is_(None),
                        Quota.key_id.is_not(None),
                        Quota.api_key.has(APIKey.project_id == project_id),
                    ),
                ),
                active_filter
            )
        )
    else:
        stmt = select(Quota).where(
            and_(
                Quota.project_id == project_id,
                Quota.user_id.is_(None),
                Quota.key_id.is_(None),
                active_filter
            )
        )

    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    
    project_quotas = result.scalars().all()
    
    if include_inherited:
        global_quotas = await get_global_quotas(session=session, active_only=active_only, options=options)
    else:
        global_quotas = []


    return global_quotas + project_quotas

async def get_quotas_for_user(
        user_id: int,
        session = None,
        include_inherited: bool = True,
        include_keys: bool = False,
    active_only: bool = False,
    options = None
) -> list[Quota]:
    """
    Retrieve quotas for a user with optional inherited and key-level quotas.

    Parameters
    ----------
    - user_id: Identifier of the user.
    - session: Optional SQLAlchemy session.
    - include_inherited: Whether global and project quotas are included.
    - include_keys: Whether key-level quotas are included.
    - active_only: Whether to restrict results to active quotas.
    - options: Optional relationship loading options.

    Returns
    -------
    - A list of Quota ORM objects.
    """
    
    if session is None:
        async with get_session() as session:
            return await get_quotas_for_user(
                user_id=user_id,
                session=session,
                include_inherited=include_inherited,
                include_keys=include_keys,
                active_only=active_only,
                options=options
            )

    active_filter = (Quota.status == Status.ACTIVE) if active_only else True
    if options is None:
        options = _get_quotas_relationship_options()

    user = await get_user_by_id(user_id=user_id, session=session)
    if user is None:
        return []

    stmt = select(Quota).where(
        and_(
            Quota.user_id == user_id,
            active_filter
        )
    )
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    user_quotas = result.scalars().all()

    if include_inherited:
        global_quotas = await get_global_quotas(session=session, active_only=active_only, options=options)
        project_quotas = []
        for permission in user.permissions:
            project_quotas += await get_quotas_for_project(
                project_id=permission.project_id,
                session=session,
                include_inherited=False,
                active_only=active_only,
                options=options
            )
    else:
        global_quotas = []
        project_quotas = []

    if include_keys:
        key_quotas = []
        for api_key in user.api_keys:
            if api_key.status != Status.ACTIVE:
                continue
            key_quotas += await get_quotas_for_api_key(
                key_id=api_key.id,
                session=session,
                include_inherited=False,
                active_only=active_only,
                options=options
            )
    else:
        key_quotas = []

    return global_quotas + project_quotas + user_quotas + key_quotas


async def get_quotas_for_api_key(
        key_id: int,
        session = None,
        include_inherited: bool = True,
    active_only: bool = False,
    options = None
) -> list[Quota]:
    """
    Retrieve quotas for an API key with optional inherited user quotas.

    Parameters
    ----------
    - key_id: Identifier of the API key.
    - session: Optional SQLAlchemy session.
    - include_inherited: Whether inherited user quotas are included.
    - active_only: Whether to restrict results to active quotas.
    - options: Optional relationship loading options.

    Returns
    -------
    - A list of Quota ORM objects.
    """

    if session is None:
        async with get_session() as session:
            return await get_quotas_for_api_key(
                key_id=key_id,
                session=session,
                include_inherited=include_inherited,
                active_only=active_only,
                options=options
            )
        
    active_filter = (Quota.status == Status.ACTIVE) if active_only else True
    if options is None:
        options = _get_quotas_relationship_options()

    key_result = await session.execute(
        select(APIKey).where(
            APIKey.id == key_id,
            APIKey.status == Status.ACTIVE,
        )
    )
    api_key = key_result.scalars().first()

    if api_key is None:
        return []

    stmt = select(Quota).where(
        and_(
            Quota.key_id == key_id,
            active_filter
        )
    )
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    api_key_quotas = result.scalars().all()
    
    if include_inherited:
        inherited_from_user = await get_quotas_for_user(
            user_id=api_key.user_id,
            session=session,
            include_inherited=True,
            active_only=active_only,
            options=options
        )
    else:
        inherited_from_user = []

    return inherited_from_user + api_key_quotas

async def create_quota(
        project_id: int | None,
        user_id: int | None,
        key_id: int | None,
        limit_id: int,
        limit_value: float | None,
        period: Period,
        expires_at: datetime | None,
        session = None
):
    """
    Create and persist a new quota record.

    Parameters
    ----------
    - project_id: Optional project identifier target.
    - user_id: Optional user identifier target.
    - key_id: Optional API key identifier target.
    - limit_id: Limit type identifier.
    - limit_value: Optional numeric quota limit.
    - period: Quota period enum value.
    - expires_at: Optional quota expiration timestamp.
    - session: Optional transactional SQLAlchemy session.

    Returns
    -------
    - The created Quota ORM object.
    """
    
    if session is None:
        async with get_transactional_session() as session:
            return await create_quota(
                project_id=project_id,
                user_id=user_id,
                key_id=key_id,
                limit_id=limit_id,
                limit_value=limit_value,
                period=period,
                expires_at=expires_at,
                session=session
            )

    new_quota = Quota(
        project_id=project_id,
        user_id=user_id,
        key_id=key_id,
        limit_id=limit_id,
        limit_value=limit_value,
        period=period,
        expires_at=expires_at,
        status=Status.ACTIVE,
        allocated=0,
        next_reset=calculate_date_after_period(period, datetime.now(timezone.utc))
    )
    session.add(new_quota)

    return new_quota

async def delete_quota(quota_id: int, session = None) -> None:
    """
    Delete a quota by identifier.

    Parameters
    ----------
    - quota_id: Identifier of the quota to delete.
    - session: Optional transactional SQLAlchemy session.

    Returns
    -------
    - None.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await delete_quota(quota_id=quota_id, session=session)

    result = await session.execute(select(Quota).where(Quota.id == quota_id).with_for_update())
    quota = result.scalars().first()
    if quota is None:
        raise ValueError("Quota not found.")

    await session.delete(quota)

def _get_quotas_relationship_options():
    """Return default relationship loading options for quota queries."""

    return (
        selectinload(Quota.project),
        selectinload(Quota.user),
        selectinload(Quota.api_key),
        selectinload(Quota.limit)
    )