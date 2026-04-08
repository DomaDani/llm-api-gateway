from sqlalchemy import select
from datetime import datetime, timezone

from shared.db import get_session, get_transactional_session
from shared.models import User

async def get_user_by_id(user_id: int) -> User | None:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))

        user_record = result.scalars().first()

        return user_record

async def get_user_by_email(email: str) -> User | None:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.email == email))

        user_record = result.scalars().first()

        return user_record

async def get_user_by_username(username: str) -> User | None:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.username == username))

        user_record = result.scalars().first()

        return user_record

async def user_email_free(email: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_email(email)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)

async def user_username_free(username: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_username(username)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)

async def change_user_identity(user_id: int, new_email: str, new_username: str) -> User:
    async with get_transactional_session() as session:
        result = await session.execute(select(User).where(User.id == user_id).with_for_update())
        user_record = result.scalars().first()

        if user_record is None:
            raise ValueError("User not found.")

        user_record.email = new_email
        user_record.username = new_username

        return user_record
    
async def change_user_password(user_id: int, new_password_hash: str) -> User:
    async with get_transactional_session() as session:
        result = await session.execute(select(User).where(User.id == user_id).with_for_update())
        user_record = result.scalars().first()

        if user_record is None:
            raise ValueError("User not found.")

        user_record.password_hash = new_password_hash
        user_record.password_expires_at = None

        return user_record
    
async def create_user(email: str, username: str, password_hash: str, mandate_reset: bool = False) -> User:
    async with get_transactional_session() as session:
        new_user = User(email=email, username=username, password_hash=password_hash, password_expires_at=datetime.now(tz=timezone.utc) if mandate_reset else None)
        session.add(new_user)

        return new_user
    
async def delete_user(user_id: int) -> None:
    async with get_transactional_session() as session:
        result = await session.execute(select(User).where(User.id == user_id).with_for_update())
        user_record = result.scalars().first()

        if user_record is None:
            raise ValueError("User not found.")

        await session.delete(user_record)