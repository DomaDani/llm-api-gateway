from sqlalchemy import select, func, or_, and_
from typing import Tuple

from shared.models import APIKey, Quota, Limit, Status
from shared.db import get_transactional_session, get_session

MAX_VALUE = 1 << 60

async def db_limit_check_and_allocation(api_key: APIKey, estimated_tokens: int, estimated_price: int) -> bool:
    async with get_transactional_session() as session:
        
        request_quotas, token_quotas, price_quotas = await db_get_quotas_by_key(api_key, session=session)

        if not request_quotas and not token_quotas and not price_quotas:
            return True # There is no active quota for the key.
        
        strictest_request_quota = min(request_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)
        strictest_token_quota = min(token_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)
        strictest_price_quota = min(price_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)

        new_allocated_request = strictest_request_quota.allocated + 1 if strictest_request_quota else 0
        new_allocated_token = strictest_token_quota.allocated + estimated_tokens if strictest_token_quota else 0
        new_allocated_price = strictest_price_quota.allocated + estimated_price if strictest_price_quota else 0

        if strictest_request_quota and strictest_request_quota.limit_value is None:
            return True
        elif strictest_request_quota and new_allocated_request > strictest_request_quota.limit_value:
            return False
        elif strictest_token_quota and new_allocated_token > strictest_token_quota.limit_value:
            return False
        elif strictest_price_quota and new_allocated_price > strictest_price_quota.limit_value:
            return False
        else:
            await db_limit_change(api_key, update_req_count=True, change_by_tokens=estimated_tokens, change_by_price=estimated_price, session=session)
            return True

async def db_limit_change(api_key: APIKey, update_req_count: bool = False, change_by_tokens: int = 0, change_by_price: int = 0, session = None):
    # Check if a session was provided, if not, create a new transactional session
    if session is None:
        async with get_transactional_session() as session:
            await db_limit_change(api_key, update_req_count, change_by_tokens, change_by_price, session=session)
            return

    request_delta = (change_by_tokens > 0) - (change_by_tokens < 0)

    request_quotas, token_quotas, price_quotas = await db_get_quotas_by_key(api_key, session=session)

    if update_req_count:
        for r_quota in request_quotas:
            if r_quota.limit_value is not None:
                r_quota.allocated = min(max(r_quota.allocated + request_delta, 0), r_quota.limit_value)
    for t_quota in token_quotas:
        if t_quota.limit_value is not None:
            t_quota.allocated = min(max(t_quota.allocated + change_by_tokens, 0), t_quota.limit_value)
    for p_quota in price_quotas:
        if p_quota.limit_value is not None:
            p_quota.allocated = min(max(p_quota.allocated + change_by_price, 0), p_quota.limit_value)

# Returns a tuple of the different quota types (request, token, price) for a given key.
async def db_get_quotas_by_key(api_key: APIKey, session = None) -> Tuple[list[Quota], list[Quota], list[Quota]]:
    # Check if a session was provided, if not, create a new transactional session
    if session is None:
        # Session is transactional to use locks.
        async with get_transactional_session() as session:
            return await db_get_quotas_by_key(api_key, session=session)
        
    request_limit_id, token_limit_id, price_limit_id = await _get_limit_ids(session=session)

    result = await session.execute(
        select(Quota)
        .where(_quota_filter(api_key) and Quota.status == Status.ACTIVE)
        .order_by(Quota.id)
        .with_for_update()
    )
    quotas = result.scalars().all()

    request_quotas = [q for q in quotas if q.limit_id == request_limit_id] if request_limit_id else []
    token_quotas = [q for q in quotas if q.limit_id == token_limit_id] if token_limit_id else []
    price_quotas = [q for q in quotas if q.limit_id == price_limit_id] if price_limit_id else []

    return request_quotas, token_quotas, price_quotas

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

# Returns a tuple of the different limit IDs (request, token, price).
async def _get_limit_ids(session = None) -> Tuple[int, int, int]:
    if session is None:
        async with get_session() as session:
            return await _get_limit_ids(session=session)

    result = await session.execute(
    select(Limit)
    .where(Limit.name == "Request Limit")
    .order_by(Limit.id)
    )

    request_limit = result.scalars().one_or_none()
    request_limit_id = request_limit.id if request_limit else None

    result = await session.execute(
        select(Limit)
        .where(Limit.name == "Token Limit")
        .order_by(Limit.id)
    )

    token_limit = result.scalars().one_or_none()
    token_limit_id = token_limit.id if token_limit else None

    result = await session.execute(
        select(Limit)
        .where(Limit.name == "Price Limit")
        .order_by(Limit.id)
    )

    price_limit = result.scalars().one_or_none()
    price_limit_id = price_limit.id if price_limit else None

    return request_limit_id, token_limit_id, price_limit_id