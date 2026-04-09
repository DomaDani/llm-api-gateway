from sqlalchemy import select

from shared.db import get_session
from shared.models import User


async def get_user_by_id(user_id: int, session = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_id(user_id=user_id, session=session)

    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(email: str, session = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_email(email=email, session=session)

    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_username(username: str, session = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_username(username=username, session=session)

    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def user_email_free(email: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_email(email)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)


async def user_username_free(username: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_username(username)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)