from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import User, Status

from .permissions import is_user_project_manager, is_user_administrator
from .keys import delete_key
from .quotas import delete_quota

async def change_user_identity(user_id: int, new_email: str, new_username: str) -> User:
    """
    Update a user's email and username.

    Parameters
    ----------
    - user_id: Identifier of the user.
    - new_email: New email value.
    - new_username: New username value.

    Returns
    -------
    - The updated User ORM object.
    """
    async with get_transactional_session() as session:
        result = await session.execute(select(User).where(User.id == user_id).with_for_update())
        user = result.scalars().first()

        if user is None:
            raise ValueError("User not found.")

        user.email = new_email
        user.username = new_username

        return user
    
async def change_user_password(user_id: int, new_password_hash: str, mandate_reset: bool = False) -> User:
    """
    Update a user's password hash and optional reset flag timestamp.

    Parameters
    ----------
    - user_id: Identifier of the user.
    - new_password_hash: New hashed password value.
    - mandate_reset: Whether password expiration should be set immediately.

    Returns
    -------
    - The updated User ORM object.
    """
    async with get_transactional_session() as session:
        result = await session.execute(select(User).where(User.id == user_id).with_for_update())
        user = result.scalars().first()

        if user is None:
            raise ValueError("User not found.")

        user.password_hash = new_password_hash
        user.password_expires_at = datetime.now(timezone.utc) if mandate_reset else None

        return user
    
async def create_user(email: str, username: str, password_hash: str, mandate_reset: bool = False, session = None) -> User:
    """
    Create and persist a new user record.

    Parameters
    ----------
    - email: User email address.
    - username: User username.
    - password_hash: Hashed password value.
    - mandate_reset: Whether password expiration is set at creation.
    - session: Optional transactional SQLAlchemy session.

    Returns
    -------
    - The created User ORM object.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await create_user(email=email, username=username, password_hash=password_hash, mandate_reset=mandate_reset, session=session)

    new_user = User(
        email=email,
        username=username,
        password_hash=password_hash,
        joined_date=datetime.now(timezone.utc),
        password_expires_at=datetime.now(timezone.utc) if mandate_reset else None
    )
    session.add(new_user)
    
    return new_user
    
async def delete_user(user_id: int, session = None) -> None:
    """
    Delete a user and cleanup related permissions, keys, and quotas.

    Parameters
    ----------
    - user_id: Identifier of the user to delete.
    - session: Optional transactional SQLAlchemy session.

    Returns
    -------
    - None.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await delete_user(user_id=user_id, session=session)

    result = await session.execute(
        select(User)
        .where(User.id == user_id)
        .with_for_update()
        .options(
            selectinload(User.permissions),
            selectinload(User.api_keys),
            selectinload(User.quotas),
        )
    )
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
        if api_key.status == Status.ACTIVE:
            await delete_key(key_id=api_key.id, session=session)
    for quota in user.quotas:
        await delete_quota(quota_id=quota.id, session=session)

    await session.delete(user)

async def get_all_users(session = None) -> list[User]:
    """
    Retrieve all users ordered by username.

    Parameters
    ----------
    - session: Optional SQLAlchemy session.

    Returns
    -------
    - A list of User ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_all_users(session=session)

    result = await session.execute(select(User).order_by(User.username))
    return result.scalars().all()

async def is_password_expired(user_id: int, session = None) -> bool:
    """
    Check whether a user's password expiration timestamp has passed.

    Parameters
    ----------
    - user_id: Identifier of the user.
    - session: Optional SQLAlchemy session.

    Returns
    -------
    - True if password is expired, otherwise False.
    """
    if session is None:
        async with get_session() as session:
            return await is_password_expired(user_id=user_id, session=session)

    result = await session.execute(select(User.password_expires_at).where(User.id == user_id))
    expires_at = result.scalar_one_or_none()

    if expires_at is None:
        return False

    return expires_at < datetime.now(timezone.utc)