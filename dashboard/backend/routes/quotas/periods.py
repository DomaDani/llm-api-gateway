from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import quota_convert_period_enum_to_display_info as convert_period_enum_to_display_info
from dashboard.backend.models import PeriodDisplayInformation
from shared.models import Period

router = APIRouter(prefix="/quotas", tags=["quotas"])


@router.get("/periods", response_model=list[PeriodDisplayInformation], description="Get all available quota periods.")
async def get_periods(_: None = Depends(require_valid_access_token)) -> list[PeriodDisplayInformation]:
    """
    Retrieve all supported quota period enum values.

    Parameters
    ----------
    - _: Token validation dependency output, unused in function body.

    Returns
    -------
    - A list of period display models.
    """
    try:
        periods = list(Period)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching periods. Please try again later.") from e

    return [convert_period_enum_to_display_info(period) for period in periods]
