from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_administrator_user
from dashboard.backend.db import delete_user
from dashboard.backend.management import user_enforce_existing_user
from dashboard.backend.models import UserDeleteRequest, UserDisplayInformation

router = APIRouter(prefix="/users", tags=["users"])

@router.delete("/delete", description="Delete a user by id.")
async def delete_user_route(
    request: UserDeleteRequest,
    _: UserDisplayInformation = Depends(require_administrator_user),
):
    await user_enforce_existing_user(request.user_id)

    try:
        await delete_user(user_id=request.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while deleting user. Please try again later.") from e

    return {"message": f"User deleted successfully."}
