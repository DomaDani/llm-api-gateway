from sqlalchemy import select
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import User

from .permissions import is_user_project_manager, is_user_administrator
from .keys import delete_key
from .quotas import delete_quota

async def get_user_by_id(user_id: int, session = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_id(user_id=user_id, session=session)
        
    result = await session.execute(select(User).where(User.id == user_id))

    user = result.scalars().first()

    return user

async def get_user_by_email(email: str, session = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_email(email=email, session=session)

    result = await session.execute(select(User).where(User.email == email))

    user = result.scalars().first()

    return user

async def get_user_by_username(username: str, session = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_username(username=username, session=session)

    result = await session.execute(select(User).where(User.username == username))

    user = result.scalars().first()

    return user

async def user_email_free(email: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_email(email)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)

async def user_username_free(username: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_username(username)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)

async def change_user_identity(user_id: int, new_email: str, new_username: str) -> User:
    async with get_transactional_session() as session:
        result = await session.execute(select(User).where(User.id == user_id).with_for_update())
        user = result.scalars().first()

        if user is None:
            raise ValueError("User not found.")

        user.email = new_email
        user.username = new_username

        return user
    
async def change_user_password(user_id: int, new_password_hash: str) -> User:
    async with get_transactional_session() as session:
        result = await session.execute(select(User).where(User.id == user_id).with_for_update())
        user = result.scalars().first()

        if user is None:
            raise ValueError("User not found.")

        user.password_hash = new_password_hash
        user.password_expires_at = None

        return user
    
async def create_user(email: str, username: str, password_hash: str, mandate_reset: bool = False, session = None) -> User:
    if session is None:
        async with get_transactional_session() as session:
            return await create_user(email=email, username=username, password_hash=password_hash, mandate_reset=mandate_reset, session=session)

        return new_user
    
async def delete_user(user_id: int, session = None) -> None:
    if session is None:
        async with get_transactional_session() as session:
            return await delete_user(user_id=user_id, session=session)

    result = await session.execute(select(User).where(User.id == user_id).with_for_update())
    user = result.scalars().first()

    if user is None:
        raise ValueError("User not found.")
    
    if await is_user_administrator(user_id=user_id, session=session):
        raise ValueError("Cannot delete an administrator user.")
    if await is_user_project_manager(user_id=user_id, session=session):
        raise ValueError("Cannot delete a user who is a project manager. Please delete the projects they manage first.")

    for permission in user.permissions:
        await session.delete(permission)
    for api_key in user.api_keys:
        await delete_key(key_id=api_key.id, session=session)
    for quota in user.quotas:
        await delete_quota(quota_id=quota.id, session=session)

    await session.delete(user)