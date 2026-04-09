from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserPasswordChangeRequest
from dashboard.backend.auth import require_current_user
from dashboard.backend.models import UserDisplayInfo
from dashboard.backend.db import get_user_by_id
from dashboard.backend.management.users import enforce_password_change_validity
from dashboard.backend.db import change_user_password

from shared.utils.password import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/change-password", description="Change the password of the current authenticated user.")
async def change_password(
    request: UserPasswordChangeRequest,
    current_user: UserDisplayInfo = Depends(require_current_user)
):
    user_record = await get_user_by_id(current_user.id)
    if user_record is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    await enforce_password_change_validity(
        current_password=request.current_password,
        current_password_hash=user_record.password_hash,
        new_password=request.new_password,
        new_password_confirm=request.new_password_confirm,
    )

    try:
        await change_user_password(user_id=current_user.id, new_password_hash=hash_password(request.new_password))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while changing password. Please try again later.") from e

    return {"message": "Password changed successfully."}