from sqlalchemy import select, func, or_, and_
from typing import Tuple

from shared.models import APIKey, Quota, Limit, Status
from shared.db import get_transactional_session

MAX_VALUE = 1 << 60

async def db_limit_check_and_allocation(api_key: APIKey, estimate: int) -> bool:
    async with get_transactional_session() as session:
        
        request_quotas, token_quotas = await db_get_quotas_by_key(api_key, session=session)

        if not request_quotas and not token_quotas:
            return True # There is no active quota for the key.
        
        strictest_request_quota = min(request_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)
        strictest_token_quota = min(token_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)
        
        new_allocated_request = strictest_request_quota.allocated + estimate if strictest_request_quota else 0
        new_allocated_token = strictest_token_quota.allocated + estimate if strictest_token_quota else 0


        if strictest_request_quota and strictest_request_quota.limit_value is None:
            return True
        elif new_allocated_request > strictest_request_quota.limit_value:
            return False
        elif new_allocated_token > strictest_token_quota.limit_value:
            return False
        else:
            await db_limit_change(api_key, estimate, session=session)
            return True

async def db_limit_change(api_key: APIKey, change_by: int, session = None):
    # Check if a session was provided, if not, create a new transactional session
    if session is None:
        async with get_transactional_session() as session:
            await db_limit_change(api_key, change_by, session=session)
            return

    quotas, _ = await db_get_quotas_by_key(api_key, session=session)

    for quota in quotas:
        if quota.limit_value is not None:
            quota.allocated = min(max(quota.allocated + change_by, 0), quota.limit_value)

# Returns a tuple of the different quota types (request, token) for a given key.
async def db_get_quotas_by_key(api_key: APIKey, session = None) -> Tuple[list[Quota], list[Quota]]:
    # Check if a session was provided, if not, create a new transactional session
    if session is None:
        # Session is transactional to use locks.
        async with get_transactional_session() as session:
            return await db_get_quotas_by_key(api_key, session=session)
    
    result = await session.execute(
        select(Limit)
        .where(Limit.name == "Request Limit")
        .order_by(Limit.id)
    )

    request_limit_id = result.scalars().one().id

    result = await session.execute(
        select(Limit)
        .where(Limit.name == "Token Limit")
        .order_by(Limit.id)
    )

    token_limit_id = result.scalars().one().id

    result = await session.execute(
        select(Quota)
        .where(_quota_filter(api_key))
        .order_by(Quota.id)
        .with_for_update()
    )
    quotas = result.scalars().all()

    request_quotas = [q for q in quotas if q.limit_id == request_limit_id]
    token_quotas = [q for q in quotas if q.limit_id == token_limit_id]

    return request_quotas, token_quotas

def _quota_filter(api_key: APIKey):
    return and_(
        or_(
            Quota.key_id == api_key.id,
            Quota.project_id == api_key.project_id,
            Quota.user_id == api_key.user_id,
            and_(
                Quota.key_id.is_(None),
                Quota.project_id.is_(None),
                Quota.user_id.is_(None)
            )
        ),
        Quota.status == Status.ACTIVE
    )