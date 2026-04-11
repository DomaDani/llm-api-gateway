from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import QuotaDisplayInformation, QuotaInformationRequest
from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import quota_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.db import get_global_quotas, get_quotas_for_project, get_quotas_for_user, get_quotas_for_api_key

router = APIRouter(prefix="/quotas", tags=["quotas"])

@router.get("/info", response_model=list[QuotaDisplayInformation], description="Get specific information about quotas either globally, per project, per user or per API key")
async def get_user_information(request: QuotaInformationRequest = Depends(), _: None = Depends(require_valid_access_token)) -> list[QuotaDisplayInformation]:
    try:
        if request.project_id is not None:
            quota_orms = await get_quotas_for_project(
                project_id=request.project_id,
                include_targeted=True,
                active_only=request.active_only
            )
        if request.user_id is not None:
            quota_orms = await get_quotas_for_user(
                user_id=request.user_id,
                include_keys=True,
                active_only=request.active_only
            )
        if request.key_id is not None:
            quota_orms = await get_quotas_for_api_key(
                key_id=request.key_id,
                include_targeted=True,
                active_only=request.active_only
            )
        else:
            quota_orms = await get_global_quotas(active_only=request.active_only, include_targeted=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching quota information. Please try again later.") from e

    return [await convert_orm_to_display_info(quota_orm, add_name=True) for quota_orm in quota_orms]