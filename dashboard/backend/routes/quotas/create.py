from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_current_user
from dashboard.backend.db import create_quota as db_create_quota
from dashboard.backend.management import quota_convert_orm_to_display_info as convert_orm_to_display_info, quota_enforce_creation_permission, quota_enforce_existing_limit, quota_enforce_existing_quota_target
from dashboard.backend.models import QuotaCreateRequest, QuotaDisplayInformation, UserDisplayInformation

router = APIRouter(prefix="/quotas", tags=["quotas"])


@router.post("/create", response_model=QuotaDisplayInformation, description="Create a new quota.")
async def create_quota(
    request: QuotaCreateRequest,
    current_user: UserDisplayInformation = Depends(require_current_user),
) -> QuotaDisplayInformation:
    try:
        await quota_enforce_existing_limit(request.limit_id)
        await quota_enforce_existing_quota_target(request.project_id, request.user_id, request.key_id)
        await quota_enforce_creation_permission(current_user.id, request.project_id, request.user_id, request.key_id)

        created_quota = await db_create_quota(
            project_id=request.project_id,
            user_id=request.user_id,
            key_id=request.key_id,
            limit_id=request.limit_id,
            limit_value=request.limit_value,
            period=request.period,
            expires_at=request.expires_at,
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while creating quota. Please try again later.") from e

    return convert_orm_to_display_info(created_quota)
