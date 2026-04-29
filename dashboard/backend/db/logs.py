from sqlalchemy import Row, func, literal_column, select

from shared.db import get_session

from shared.models import UsageLog


async def get_usage_logs(
    user_id: int | None = None,
    project_id: int | None = None,
    aggregate_by_fifteen_minutes: bool = False,
    limit: int | None = None,
    offset: int = 0,
    session = None
) -> list[UsageLog] | list[Row]:
    """
    Retrieve usage logs with optional filtering, pagination, and aggregation.

    Parameters
    ----------
    user_id : int | None, optional
        Optional user identifier filter.
    project_id : int | None, optional
        Optional project identifier filter.
    aggregate_by_fifteen_minutes : bool, optional
        Whether to return 15-minute aggregate rows.
    limit : int | None, optional
        Optional maximum number of rows to return.
    offset : int, optional
        Number of rows to skip.
    session : optional
        Optional SQLAlchemy session.

    Returns
    -------
    list[UsageLog] | list[Row]
        A list of UsageLog ORM objects or aggregated SQL rows.
    """

    if session is None:
        async with get_session() as session:
            return await get_usage_logs(
                user_id=user_id,
                project_id=project_id,
                aggregate_by_fifteen_minutes=aggregate_by_fifteen_minutes,
                limit=limit,
                offset=offset,
                session=session
            )


    filters = _get_filter(user_id=user_id, project_id=project_id)

    if aggregate_by_fifteen_minutes:
        query = (
            select(
                _get_time_chunk(),
                UsageLog.project_id,
                UsageLog.user_id,
                UsageLog.key_id,
                func.count().label("request_count"),
                func.sum(UsageLog.total_tokens).label("total_tokens"),
                func.sum(UsageLog.internal_cost_final).label("total_cost"),
            ).where(*filters)
            .group_by(literal_column("time_chunk"), UsageLog.project_id, UsageLog.user_id, UsageLog.key_id)
            .order_by(literal_column("time_chunk").desc())
        )
        if offset:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await session.execute(query)
        return result.all()
    else:
        query = select(UsageLog).where(*filters).order_by(UsageLog.timestamp.desc())
        if offset:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

def _get_filter(
    user_id: int | None = None,
    project_id: int | None = None,
) -> list:
    """
    Build SQL filters for usage log queries.

    Parameters
    ----------
    user_id : int | None, optional
        Optional user identifier filter.
    project_id : int | None, optional
        Optional project identifier filter.

    Returns
    -------
    list
        A list of SQLAlchemy filter expressions.
    """
    
    filters = []
    if user_id is not None:
        filters.append(UsageLog.user_id == user_id)
    if project_id is not None:
        filters.append(UsageLog.project_id == project_id)
    
    return filters

def _get_time_chunk(interval : int = 15*60):
    """
    Build SQL expression for fixed-width timestamp buckets.

    Parameters
    ----------
    interval : int, optional
        Bucket width in seconds.

    Returns
    -------
    SQLAlchemy expression
        A labeled SQLAlchemy expression for grouped time chunks.
    """
    return (
        func.to_timestamp(
            (
                func.floor(func.extract("epoch", UsageLog.timestamp) / interval) * interval
            )
        )
    ).label("time_chunk")
