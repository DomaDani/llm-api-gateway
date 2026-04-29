from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.db import get_usage_logs
from dashboard.backend.management import log_convert_orm_to_display_info as convert_orm_to_display_info, log_convert_aggregate_row_to_display_info as convert_aggregate_row_to_display_info
from dashboard.backend.models import UsageLogInformationRequest, UsageLogDisplayInformation, UsageLogAggregateDisplayInformation

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get(
    "/info",
    response_model=list[UsageLogDisplayInformation] | list[UsageLogAggregateDisplayInformation],
    description="Get usage logs globally, by project, or by user. Supports optional aggregation by 15-minute chunks.",
)
async def get_log_information(
    request: UsageLogInformationRequest = Depends(),
    _: None = Depends(require_valid_access_token),
) -> list[UsageLogDisplayInformation] | list[UsageLogAggregateDisplayInformation]:
    """
    Retrieve usage logs by scope, with optional aggregation mode.

    Parameters
    ----------
    request : UsageLogInformationRequest
        Query payload with filters, pagination, and aggregation options.
    _ : None
        Token validation dependency output, unused in function body.

    Returns
    -------
    list[UsageLogDisplayInformation] | list[UsageLogAggregateDisplayInformation]
        A list of detailed usage logs or aggregated rows based on request.aggregate.
    """
    try:
        logs = await get_usage_logs(
            user_id=request.user_id,
            project_id=request.project_id,
            aggregate_by_fifteen_minutes=request.aggregate,
            limit=request.limit,
            offset=request.offset,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching usage logs. Please try again later.") from e

    if request.aggregate:
        return [await convert_aggregate_row_to_display_info(row) for row in logs]

    return [await convert_orm_to_display_info(log) for log in logs]
