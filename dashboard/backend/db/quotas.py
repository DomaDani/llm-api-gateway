from sqlalchemy import select, and_
from datetime import datetime, timezone, timedelta

from shared.db import get_session, get_transactional_session
from shared.models import Quota, Status, Period, User, Project, APIKey

async def get_quota_by_id(quota_id: int, session = None) -> Quota | None:
    if session is None:
        async with get_session() as session:
            return await get_quota_by_id(quota_id=quota_id, session=session)

    result = await session.execute(select(Quota).where(Quota.id == quota_id))
    return result.scalars().first()

async def get_global_quotas(
        session = None,
        include_targeted: bool = False,
        active_only: bool = False
) -> list[Quota]:

    if session is None:
        async with get_session() as session:
            return await get_global_quotas(
                session=session,
                include_targeted=include_targeted,
                active_only=active_only
            )

    active_filter = (Quota.status == Status.ACTIVE) if active_only else True

    if include_targeted:
        result = await session.execute(
            select(Quota).where(
                and_(
                    Quota.project_id.is_(None),
                    active_filter
                )
            )
        )
    else:
        result = await session.execute(
            select(Quota).where(
                and_(
                    Quota.user_id.is_(None),
                    Quota.project_id.is_(None),
                    Quota.key_id.is_(None),
                    active_filter
                )
            )
        )
    
    return result.scalars().all()

async def get_quotas_for_project(
        project_id: int,
        session = None,
        include_targeted: bool = False,
        include_inherited: bool = True,
        active_only: bool = False
) -> list[Quota]:
    
    if session is None:
        async with get_session() as session:
            return await get_quotas_for_project(
                project_id=project_id,
                session=session,
                include_targeted=include_targeted,
                include_inherited=include_inherited,
                active_only=active_only
            )

    active_filter = (Quota.status == Status.ACTIVE) if active_only else True

    if include_targeted:
        result = await session.execute(
            select(Quota).where(
                and_(
                    Quota.project_id == project_id,
                    active_filter
                )
            )
        )
    else:
        result = await session.execute(
            select(Quota).where(
                and_(
                    Quota.project_id == project_id,
                    Quota.user_id.is_(None),
                    Quota.key_id.is_(None),
                    active_filter
                )
            )
        )
    
    project_quotas = result.scalars().all()
    
    if include_inherited:
        global_quotas = await get_global_quotas(session=session, active_only=active_only)
    else:
        global_quotas = []


    return global_quotas + project_quotas

async def get_quotas_for_user(
        user_id: int,
        session = None,
        include_inherited: bool = True,
        include_keys: bool = False,
        active_only: bool = False
) -> list[Quota]:
    
    if session is None:
        async with get_session() as session:
            return await get_quotas_for_user(
                user_id=user_id,
                session=session,
                include_inherited=include_inherited,
                include_keys=include_keys,
                active_only=active_only
            )

    active_filter = (Quota.status == Status.ACTIVE) if active_only else True

    user_result = await session.execute(select(User).where(User.id == user_id))
    user = user_result.scalars().first()
    if user is None:
        return []

    result = await session.execute(
        select(Quota).where(
            and_(
                Quota.user_id == user_id,
                active_filter
            )
        )
    )
    user_quotas = result.scalars().all()

    if include_inherited:
        global_quotas = await get_global_quotas(session=session, active_only=active_only)
        project_quotas = []
        for permission in user.permissions:
            project_quotas += await get_quotas_for_project(
                project_id=permission.project_id,
                session=session,
                include_inherited=False,
                active_only=active_only
            )
    else:
        global_quotas = []
        project_quotas = []

    if include_keys:
        key_quotas = []
        for api_key in user.api_keys:
            key_quotas += await get_quotas_for_api_key(
                key_id=api_key.id,
                session=session,
                include_inherited=False,
                active_only=active_only
            )
    else:
        key_quotas = []

    return global_quotas + project_quotas + user_quotas + key_quotas


async def get_quotas_for_api_key(
        key_id: int,
        session = None,
        include_inherited: bool = True,
        active_only: bool = False
) -> list[Quota]:

    if session is None:
        async with get_session() as session:
            return await get_quotas_for_api_key(
                key_id=key_id,
                session=session,
                include_inherited=include_inherited,
                active_only=active_only
            )
        
    active_filter = (Quota.status == Status.ACTIVE) if active_only else True

    key_result = await session.execute(select(APIKey).where(APIKey.id == key_id))
    api_key = key_result.scalars().first()

    if api_key is None:
        return []

    result = await session.execute(
        select(Quota).where(
            and_(
                Quota.key_id == key_id,
                active_filter
            )
        )
    )
    api_key_quotas = result.scalars().all()
    
    if include_inherited:
        inherited_from_user = await get_quotas_for_user(
            user_id=api_key.user_id,
            session=session,
            include_inherited=True,
            active_only=active_only
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
        next_reset=datetime.now(timezone.utc) + timedelta(seconds=period.value)
    )
    session.add(new_quota)

    return new_quota

async def delete_quota(quota_id: int, session = None) -> None:
    if session is None:
        async with get_transactional_session() as session:
            return await delete_quota(quota_id=quota_id, session=session)

    quota = await get_quota_by_id(quota_id=quota_id, session=session)
    if quota is None:
        raise ValueError("Quota not found.")

    await session.delete(quota)