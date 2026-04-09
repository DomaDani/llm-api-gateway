from sqlalchemy import select
from sqlalchemy.orm import selectinload

from shared.db import get_session
from shared.models import User, ProjectPermission


async def get_user_by_id(user_id: int, session = None, options = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_id(user_id=user_id, session=session, options=options)

    stmt = select(User).where(User.id == user_id)
    if options is None:
        options = get_user_relationship_options()
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(email: str, session = None, options = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_email(email=email, session=session, options=options)

    stmt = select(User).where(User.email == email)
    if options is None:
        options = get_user_relationship_options()
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_username(username: str, session = None, options = None) -> User | None:
    if session is None:
        async with get_session() as session:
            return await get_user_by_username(username=username, session=session, options=options)

    stmt = select(User).where(User.username == username)
    if options is None:
        options = get_user_relationship_options()
    if options:
        stmt = stmt.options(*options)

    result = await session.execute(stmt)
    return result.scalars().first()


async def user_email_free(email: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_email(email)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)


async def user_username_free(username: str, exclude_user_id: int | None = None) -> bool:
    user = await get_user_by_username(username)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)


def get_user_relationship_options():
    return (
        selectinload(User.permissions).selectinload(ProjectPermission.project),
        selectinload(User.permissions).selectinload(ProjectPermission.role),
        selectinload(User.api_keys),
        selectinload(User.quotas),
    )