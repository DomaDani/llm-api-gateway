from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_current_user
from dashboard.backend.db import delete_key as db_delete_key
from dashboard.backend.management import key_enforce_deletion_permission
from dashboard.backend.models import ApiKeyDeleteRequest, UserDisplayInformation

router = APIRouter(prefix="/keys", tags=["keys"])


@router.delete("/delete", description="Archive an API key by id.")
async def delete_api_key(
    request: ApiKeyDeleteRequest,
    current_user: UserDisplayInformation = Depends(require_current_user),
):
    try:
        await key_enforce_deletion_permission(current_user_id=current_user.id, key_id=request.key_id)

        await db_delete_key(key_id=request.key_id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while deleting API key. Please try again later.") from e

    return {"message": "API key archived successfully."}
