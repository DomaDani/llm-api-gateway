from sqlalchemy import select, func, text

from shared.db import get_transactional_session
from shared.models import Quota, Status
from shared.utils import calculate_date_after_period


async def refresh_quotas_by_batch(session=None, batch_size: int = 100):
    if session is None:
        async with get_transactional_session() as session:
            return await refresh_quotas_by_batch(session=session, batch_size=batch_size)

    await session.execute(text("SELECT pg_advisory_xact_lock(hashtext('gateway.db.refresh')::bigint);"))

    total = 0
    while True:
        q_stmt = (
        select(Quota)
        .where(Quota.next_reset <= func.now(), Quota.allocated != 0)
        .with_for_update()
        .limit(batch_size)
        )
        res = await session.execute(q_stmt)
        rows = res.scalars().all()
        if not rows:
            break
        for q in rows:
            q.allocated = 0
            q.next_reset = calculate_date_after_period(q.period, q.next_reset)
            total += 1

    return total

async def expire_quotas_by_batch(session=None, batch_size: int = 100):
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
