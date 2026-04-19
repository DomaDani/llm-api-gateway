from sqlalchemy import select, func
from shared.models import Quota
from shared.db import get_transactional_session


async def get_quota_count(session=None) -> int:
    """
    Calculate the total number of quota entries in the database.
    If a session is provided, it uses that session; otherwise, it creates a new transactional session for the query.

    Parameters
    ----------
    - session: An optional SQLAlchemy session to use for the database query. If None, a new session will be created.

    Returns
    -------
    - int: The total number of quota entries in the database.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await get_quota_count(session=session)

    count_stmt = select(func.count()).select_from(Quota)
    res = await session.execute(count_stmt)
    count = res.scalar_one()
    return count