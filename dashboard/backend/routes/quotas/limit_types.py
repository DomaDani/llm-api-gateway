from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.db import get_all_limits
from dashboard.backend.management import quota_convert_limit_orm_to_display_info as convert_limit_orm_to_display_info
from dashboard.backend.models import LimitTypeDisplayInformation

router = APIRouter(prefix="/quotas", tags=["quotas"])


@router.get("/limit-types", response_model=list[LimitTypeDisplayInformation], description="Get all available limit types.")
async def get_limit_types(_: None = Depends(require_valid_access_token)) -> list[LimitTypeDisplayInformation]:
    try:
        limit_orms = await get_all_limits()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching limit types. Please try again later.") from e

    return [convert_limit_orm_to_display_info(limit_orm) for limit_orm in limit_orms]
