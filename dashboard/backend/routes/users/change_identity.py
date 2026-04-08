from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_current_user
from dashboard.backend.models import UserDisplayInfo, UserIdentityChangeRequest
from dashboard.backend.management.users import enforce_availability
from dashboard.backend.db.users import change_user_identity

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/change-identity", description="Change the email and/or username of the current authenticated user.")
async def change_identity(
    request: UserIdentityChangeRequest,
    current_user: UserDisplayInfo = Depends(require_current_user)
):
    await enforce_availability(email=request.email, username=request.username, exclude_user_id=current_user.id)

    try:
        await change_user_identity(user_id=current_user.id, new_email=request.email, new_username=request.username)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while changing user identity. Please try again later.") from e

    return {"message": "User identity changed successfully."}