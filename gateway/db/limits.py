from sqlalchemy import select, func, or_, and_
from typing import Tuple

from shared.models import APIKey, Quota, Limit, Status
from shared.db import get_transactional_session, get_session

MAX_VALUE = 1 << 60

async def db_limit_check_and_allocation(api_key: APIKey, estimated_tokens: int, estimated_price: float) -> bool:
    """
    Checks if the quotas for a given API key allow for the estimated tokens/price, if so, allocates them.
    The function is designed to be atomic by using a transactional session and row-level locks on the relevant quotas.

    Parameters
    ----------
    api_key : APIKey
        The APIKey ORM object for which the quotas should be checked and allocated.
    estimated_tokens : int
        The estimated number of tokens that the request will consume, used for token quota checking.
    estimated_price : float
        The estimated price of the request, used for price quota checking.

    Returns
    -------
    bool
        True if the request is within the quotas and the estimated tokens/price have been allocated, False if any quota would be exceeded.
    """
    async with get_transactional_session() as session:
        
        request_quotas, token_quotas, price_quotas = await db_get_quotas_by_key(api_key, session=session)

        if not request_quotas and not token_quotas and not price_quotas:
            return True # There is no active quota for the key.
        
        # Find the strictest quota for each type (the one closest to being exceeded) to check against.
        strictest_request_quota = min(request_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)
        strictest_token_quota = min(token_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)
        strictest_price_quota = min(price_quotas, key=lambda q: (q.limit_value or MAX_VALUE) - q.allocated, default=None)

        # Calculate the new allocated values if this request were to be allowed
        new_allocated_request = strictest_request_quota.allocated + 1 if strictest_request_quota else 0
        new_allocated_token = strictest_token_quota.allocated + estimated_tokens if strictest_token_quota else 0
        new_allocated_price = strictest_price_quota.allocated + estimated_price if strictest_price_quota else 0

        # Check if any of the strictest quotas would be exceeded by the new allocated values
        # If a quota has no limit (limit_value is None), it is considered unlimited and will not block the request.
        # The order of checks gives priority to request count, then tokens, then price, but all must be within limits for the request to be allowed.
        # Finally, the quotas are updated atomically within the same transaction.
        if (
            (strictest_request_quota is None or strictest_request_quota.limit_value is None) and
            (strictest_token_quota is None or strictest_token_quota.limit_value is None) and
            (strictest_price_quota is None or strictest_price_quota.limit_value is None)
        ):
            return True
        elif (
            (strictest_request_quota and strictest_request_quota.limit_value is not None and new_allocated_request > strictest_request_quota.limit_value) or
            (strictest_token_quota and strictest_token_quota.limit_value is not None and new_allocated_token > strictest_token_quota.limit_value) or
            (strictest_price_quota and strictest_price_quota.limit_value is not None and new_allocated_price > strictest_price_quota.limit_value)
        ):
            return False
        else:
            await db_limit_change(api_key, request_delta=1, change_by_tokens=estimated_tokens, change_by_price=estimated_price, session=session)
            return True

async def db_limit_change(api_key: APIKey, request_delta: int = 0, change_by_tokens: int = 0, change_by_price: float = 0, session = None):
    """
    Update all relevant quotas for a given API key by the specified values. 
    The function is designed to be atomic by using a transactional session and row-level locks on the relevant quotas.

    Parameters
    ----------
    api_key : APIKey
        The APIKey ORM object for which the quotas should be updated.
    request_delta : int, optional
        The change in the number of requests to allocate (positive to allocate, negative to deallocate).
    change_by_tokens : int, optional
        The change in the number of tokens to allocate (positive to allocate, negative to deallocate).
    change_by_price : float, optional
        The change in the price to allocate (positive to allocate, negative to deallocate).
    session : optional
        An optional SQLAlchemy session to use for the database operations. If None, a new transactional session will be created for this operation.
    """
    # Check if a session was provided, if not, create a new transactional session
    if session is None:
        async with get_transactional_session() as session:
            await db_limit_change(api_key, request_delta, change_by_tokens, change_by_price, session=session)
            return

    request_quotas, token_quotas, price_quotas = await db_get_quotas_by_key(api_key, session=session)

    if request_delta:
        for r_quota in request_quotas:
            if r_quota.limit_value is not None:
                r_quota.allocated = min(max(r_quota.allocated + request_delta, 0), r_quota.limit_value)
    for t_quota in token_quotas:
        if t_quota.limit_value is not None:
            t_quota.allocated = min(max(t_quota.allocated + change_by_tokens, 0), t_quota.limit_value)
    for p_quota in price_quotas:
        if p_quota.limit_value is not None:
            p_quota.allocated = min(max(p_quota.allocated + change_by_price, 0), p_quota.limit_value)


async def db_get_quotas_by_key(api_key: APIKey, session = None) -> Tuple[list[Quota], list[Quota], list[Quota]]:
    """
    Returns a tuple of the different quota types (request, token, price) for a given key.
    The function is designed to be atomic by using a transactional session and row-level locks on the relevant quotas.

    Parameters
    ----------
    api_key : APIKey
        The APIKey ORM object for which the quotas should be retrieved.
    session : optional
        An optional SQLAlchemy session to use for the database operations. If None, a new transactional session will be created for this operation.

    Returns
    -------
    Tuple[list[Quota], list[Quota], list[Quota]]
        A tuple containing three lists of Quota objects: (request_quotas, token_quotas, price_quotas) that are relevant to the given API key.
    """
    # Check if a session was provided, if not, create a new transactional session
    if session is None:
        # Session is transactional to use locks.
        async with get_transactional_session() as session:
            return await db_get_quotas_by_key(api_key, session=session)
        
    request_limit_id, token_limit_id, price_limit_id = await _get_limit_ids(session=session)

    result = await session.execute(
        select(Quota)
        .where(_quota_filter(api_key))
        .order_by(Quota.id)
        .with_for_update()
    )
    quotas = result.scalars().all()

    request_quotas = [q for q in quotas if q.limit_id == request_limit_id] if request_limit_id else []
    token_quotas = [q for q in quotas if q.limit_id == token_limit_id] if token_limit_id else []
    price_quotas = [q for q in quotas if q.limit_id == price_limit_id] if price_limit_id else []

    return request_quotas, token_quotas, price_quotas

def _quota_filter(api_key: APIKey):
    """
    Creates an SQLAlchemy filter condition to retrieve relevant quotas for a given API Key.
    A Quota is considered relevant if:
    - It is active (Quota.status == Status.ACTIVE), **AND**
    - It is directly targeting the API Key (i.e., the quota's key_id matches the API Key's id) and is either global (has no project_id) or matches the API Key's project_id, **OR**
    - It is targeting the API Key's project (i.e., the quota's project_id matches the API Key's project_id) and isn't specifically targeting a user or key (i.e., has no user_id and no key_id), **OR**
    - It is targeting the API Key's user (i.e., the quota's user_id matches the API Key's user_id) and is either global (has no project_id) or matches the API Key's project_id, **OR**
    - It is a global quota (i.e., has no key_id, no project_id, and no user_id).
    """
    return and_(
        Quota.status == Status.ACTIVE,
        or_(
            and_(
                Quota.key_id == api_key.id,
                or_(
                    Quota.project_id == api_key.project_id,
                    Quota.project_id.is_(None)
                )
            ),
            and_(
                Quota.project_id == api_key.project_id,
                Quota.user_id.is_(None),
                Quota.key_id.is_(None)
            ),
            and_(
                Quota.user_id == api_key.user_id,
                or_(
                    Quota.project_id == api_key.project_id,
                    Quota.project_id.is_(None)
                )
            ),
            and_(
                Quota.key_id.is_(None),
                Quota.project_id.is_(None),
                Quota.user_id.is_(None)
            )
        )
    )

async def _get_limit_ids(session = None) -> Tuple[int, int, int]:
    """
    Helper function that returns a tuple of the different limit IDs (request, token, price).

    Parameters
    ----------
	session : optional
	    An optional SQLAlchemy session to use for the database operations. If None, a new session will be created for this operation.

    Returns
    -------
	Tuple[int, int, int]
	    A tuple containing the IDs of the request limit, token limit, and price limit in the database. If a limit type is not found, its corresponding ID will be None.
    """
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