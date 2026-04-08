from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.models import UserIdentityChangeRequest
from dashboard.backend.management.users import enforce_availability
from dashboard.backend.db.users import change_user_identity

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/change-identity", description="Change the email and/or username of the current authenticated user.")
async def change_identity(
    request: UserIdentityChangeRequest,
    _: bool = Depends(require_valid_access_token)
):
    await enforce_availability(email=request.email, username=request.username)

    try:
        await change_user_identity(user_id=request.id, email=request.email, username=request.username)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while changing user identity. Please try again later.") from e

    return {"message": "User identity changed successfully."}