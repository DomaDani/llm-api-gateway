from sqlalchemy import select
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import APIKey, Project, User, Status

async def get_key_by_id(key_id: int, session = None) -> APIKey | None:
    if session is None:
        async with get_session() as session:
            return await get_key_by_id(key_id=key_id, session=session)

    result = await session.execute(select(APIKey).where(APIKey.id == key_id))
    return result.scalars().first()

async def get_keys_for_user(user_id: int, session = None) -> list[APIKey]:
    if session is None:
        async with get_session() as session:
            return await get_keys_for_user(user_id=user_id, session=session)

    result = await session.execute(select(APIKey).where(APIKey.user_id == user_id))
    return result.scalars().all()

async def get_keys_for_project(project_id: int, session = None) -> list[APIKey]:
    if session is None:
        async with get_session() as session:
            return await get_keys_for_project(project_id=project_id, session=session)

    result = await session.execute(select(APIKey).where(APIKey.project_id == project_id))
    return result.scalars().all()

async def get_all_keys(session = None) -> list[APIKey]:
    if session is None:
        async with get_session() as session:
            return await get_all_keys(session=session)

    result = await session.execute(select(APIKey).order_by(APIKey.name))
    return result.scalars().all()

async def create_key(
        project_id: int,
        user_id: int,
        name: str,
        fingerprint: str,
        key_hash: str,
        session = None
) -> APIKey:
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
        created_date=datetime.now(timezone.utc),
        status=Status.ACTIVE
    )

    session.add(key)

    return key

async def delete_key(key_id: int, session = None) -> None:
    if session is None:
        async with get_transactional_session() as session:
            return await delete_key(key_id=key_id, session=session)

    result = await session.execute(select(APIKey).where(APIKey.id == key_id).with_for_update())
    key = result.scalars().first()
    if key is None:
        raise ValueError("API Key not found.")
    
    for quota in key.quotas:
        await session.delete(quota)

    await session.delete(key)

async def get_key_ownership(key_id: int, session = None) -> tuple[Project, User]:
    if session is None:
        async with get_session() as session:
            return await get_key_ownership(key_id=key_id, session=session)

    result = await session.execute(select(APIKey).where(APIKey.id == key_id))

    key = result.scalars().first()

    if key is None:
        raise ValueError("API Key not found.")
    
    return (key.project, key.user)