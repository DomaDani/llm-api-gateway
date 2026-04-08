from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserPasswordChangeRequest
from dashboard.backend.auth import hash_password, require_valid_access_token
from dashboard.backend.management.users import enforce_password_change_validity
from dashboard.backend.db.users import change_user_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/change-password", description="Change the password of the current authenticated user.")
async def change_password(
    request: UserPasswordChangeRequest,
    _: bool = Depends(require_valid_access_token)
):
    await enforce_password_change_validity(request)

    try:
        await change_user_password(new_password_hash=hash_password(request.new_password))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while changing password. Please try again later.") from e

    return {"message": "Password changed successfully."}