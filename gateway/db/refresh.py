from sqlalchemy import select, func, text

from shared.db import get_transactional_session
from shared.models import Quota, Status
from shared.utils import calculate_date_after_period


async def refresh_quotas_by_batch(session=None, batch_size: int = 100):
    """
    Refreshes quotas in the database by resetting the allocated amounts and updating next reset time if the next reset time has passed.
    This function processes quotas in batches to avoid locking too many rows at once.

    Parameters
    ----------
    session : optional
        An optional SQLAlchemy session to use for the database operations. If None, a new transactional session will be created for the operation.
    batch_size : int, optional
        The number of quota records to process in each batch. Default is 100.

    Returns
    -------
    int
        The total number of quotas that were refreshed.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await refresh_quotas_by_batch(session=session, batch_size=batch_size)

    await session.execute(text("SELECT pg_advisory_xact_lock(hashtext('gateway.db.refresh')::bigint);"))

    total = 0
    while True:
        q_stmt = (
        select(Quota)
        .where(Quota.next_reset <= func.now())
        .with_for_update()
        .limit(batch_size)
        )
        res = await session.execute(q_stmt)
        rows = res.scalars().all()
        if not rows:
            break
        for q in rows:
            q.allocated = 0
            q.next_reset = calculate_date_after_period(q.period, q.next_reset, fast_forward=True)
            total += 1

    return total

async def expire_quotas_by_batch(session=None, batch_size: int = 100):
    """
    Expires quotas in the database by updating their status to EXPIRED if the expiration time has passed.
    This function processes quotas in batches to avoid locking too many rows at once.

    Parameters
    ----------
    session : optional
        An optional SQLAlchemy session to use for the database operations. If None, a new transactional session will be created for the operation.
    batch_size : int, optional
        The number of quota records to process in each batch. Default is 100.

    Returns
    -------
    int
        The total number of quotas that were expired.
    """
    if session is None:
        async with get_transactional_session() as session:
            return await expire_quotas_by_batch(session=session, batch_size=batch_size)

    await session.execute(text("SELECT pg_advisory_xact_lock(hashtext('gateway.db.refresh')::bigint);"))

    total = 0
    while True:
        q_stmt = (
        select(Quota)
        .where(Quota.expires_at <= func.now(), Quota.status != Status.EXPIRED)
        .with_for_update()
        .limit(batch_size)
        )
        res = await session.execute(q_stmt)
        rows = res.scalars().all()
        if not rows:
            break
        for q in rows:
            q.status = Status.EXPIRED
            total += 1
            
    return total
