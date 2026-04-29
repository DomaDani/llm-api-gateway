from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_current_user
from dashboard.backend.db import delete_quota as db_delete_quota
from dashboard.backend.management import quota_enforce_deletion_permission
from dashboard.backend.models import QuotaDeleteRequest, UserDisplayInformation

router = APIRouter(prefix="/quotas", tags=["quotas"])


@router.delete("/delete", description="Delete a quota by id.")
async def delete_quota(
    request: QuotaDeleteRequest,
    current_user: UserDisplayInformation = Depends(require_current_user),
):
    """
    Delete a quota after validating the current user's permission.

    Parameters
    ----------
    request : QuotaDeleteRequest
        Quota deletion payload containing the quota identifier.
    current_user : UserDisplayInformation
        Authenticated user requesting the deletion.

    Returns
    -------
    dict
        A success message dictionary when deletion completes.
    """
    try:
        await quota_enforce_deletion_permission(current_user_id=current_user.id, quota_id=request.id)
        await db_delete_quota(quota_id=request.id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while deleting quota. Please try again later.") from e

    return {"message": "Quota deleted successfully."}
