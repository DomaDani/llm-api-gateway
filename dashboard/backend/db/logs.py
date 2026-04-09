from sqlalchemy import Integer, func, literal_column, select, Row

from shared.db import get_session

from shared.models import UsageLog


async def get_usage_logs(
    user_id: int | None = None,
    project_id: int | None = None,
    aggregate_by_fifteen_minutes: bool = False,
    session = None
) -> list[UsageLog] | list[Row]:

    if session is None:
        async with get_session() as session:
            return await get_usage_logs(
                user_id=user_id,
                project_id=project_id,
                aggregate_by_fifteen_minutes=aggregate_by_fifteen_minutes,
                session=session
            )

    filters = _get_filter(user_id=user_id, project_id=project_id)

    if aggregate_by_fifteen_minutes:
        result = await session.execute(
            select(
                _get_time_chunk(),
                UsageLog.project_id,
                UsageLog.user_id,
                func.count().label("request_count"),
                func.sum(UsageLog.total_tokens).label("total_tokens"),
                func.sum(UsageLog.internal_cost_final).label("total_cost"),
            ).where(*filters)
            .group_by(literal_column("time_chunk"), UsageLog.project_id, UsageLog.user_id)
            .order_by(literal_column("time_chunk").desc())
        )
    else:
        result = await session.execute(select(UsageLog).where(*filters).order_by(UsageLog.timestamp.desc()))

    return result.all()

def _get_filter(
    user_id: int | None = None,
    project_id: int | None = None,
) -> list:
    
    filters = []
    if user_id is not None:
        filters.append(UsageLog.user_id == user_id)
    if project_id is not None:
        filters.append(UsageLog.project_id == project_id)
    
    return filters

def _get_time_chunk(interval : int = 15*60):
    return (
        func.to_timestamp(
            (
                func.floor(func.extract("epoch", UsageLog.timestamp) / interval) * interval
            )
        )
    ).label("time_chunk")
