from sqlalchemy import select
from sqlalchemy.orm import selectinload

from shared.db import get_session
from shared.models import User, ProjectPermission, Limit


async def get_user_by_id(user_id: int, session = None, options = None) -> User | None:
    """
    Retrieve a user by identifier.

    Parameters
    ----------
    user_id : int
        Identifier of the user.
    session : optional
        Optional SQLAlchemy session.
    options : optional
        Optional relationship loading options.

    Returns
    -------
    User | None
        The matching User ORM object, or None.
    """
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
    """
    Retrieve a user by email address.

    Parameters
    ----------
    email : str
        Email address to search for.
    session : optional
        Optional SQLAlchemy session.
    options : optional
        Optional relationship loading options.

    Returns
    -------
    User | None
        The matching User ORM object, or None.
    """
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
    """
    Retrieve a user by username.

    Parameters
    ----------
    username : str
        Username to search for.
    session : optional
        Optional SQLAlchemy session.
    options : optional
        Optional relationship loading options.

    Returns
    -------
    User | None
        The matching User ORM object, or None.
    """
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
    """
    Check whether an email address is available.

    Parameters
    ----------
    email : str
        Email address to validate.
    exclude_user_id : int | None, optional
        Optional user id to ignore in uniqueness checks.

    Returns
    -------
    bool
        True if the email can be used, otherwise False.
    """
    user = await get_user_by_email(email)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)


async def user_username_free(username: str, exclude_user_id: int | None = None) -> bool:
    """
    Check whether a username is available.

    Parameters
    ----------
    username : str
        Username to validate.
    exclude_user_id : int | None, optional
        Optional user id to ignore in uniqueness checks.

    Returns
    -------
    bool
        True if the username can be used, otherwise False.
    """
    user = await get_user_by_username(username)
    return user is None or (exclude_user_id is not None and user.id == exclude_user_id)

async def get_users_by_project(project_id: int, session = None) -> list[User]:
    """
    Retrieve users assigned to a project.

    Parameters
    ----------
    project_id : int
        Identifier of the project.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    list[User]
        A list of User ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_users_by_project(project_id=project_id, session=session)

    result = await session.execute(
        select(User)
        .join(ProjectPermission)
        .where(ProjectPermission.project_id == project_id)
        .order_by(User.username)
        .options(selectinload(User.permissions))
    )
    return result.scalars().all()

async def get_limit_by_id(limit_id: int, session = None) -> Limit | None:
    """
    Retrieve a quota limit type by identifier.

    Parameters
    ----------
    limit_id : int
        Identifier of the limit type.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    Limit | None
        The matching Limit ORM object, or None.
    """
    if session is None:
        async with get_session() as session:
            return await get_limit_by_id(limit_id=limit_id, session=session)

    result = await session.execute(select(Limit).where(Limit.id == limit_id))
    return result.scalars().first()


async def get_all_limits(session = None) -> list[Limit]:
    """
    Retrieve all quota limit types.

    Parameters
    ----------
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    list[Limit]
        A list of Limit ORM objects.
    """
    if session is None:
        async with get_session() as session:
            return await get_all_limits(session=session)

    result = await session.execute(select(Limit).order_by(Limit.name))
    return result.scalars().all()

def get_user_relationship_options():
    """Return default relationship loading options for user queries."""

    return (
        selectinload(User.permissions).selectinload(ProjectPermission.project),
        selectinload(User.permissions).selectinload(ProjectPermission.role),
        selectinload(User.api_keys),
        selectinload(User.quotas),
    )