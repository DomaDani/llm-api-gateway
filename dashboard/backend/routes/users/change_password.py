from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserPasswordChangeRequest
from dashboard.backend.auth import require_current_user
from dashboard.backend.models import UserDisplayInformation
from dashboard.backend.db import get_user_by_id, change_user_password, is_user_administrator
from dashboard.backend.management.users import enforce_password_change_validity, enforce_existing_user, enforce_password_strength

from shared.utils.password import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/change-password", description="Change the password of the current authenticated user.")
async def change_password(
    request: UserPasswordChangeRequest,
    current_user: UserDisplayInformation = Depends(require_current_user)
):
    user_record = await get_user_by_id(current_user.id)
    if user_record is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    id_to_use = current_user.id

    if request.user_id is not None:
        if not await is_user_administrator(current_user.id):
            raise HTTPException(status_code=403, detail="Only administrators can change other users' passwords.")
        
        await enforce_password_strength(request.new_password)
        await enforce_existing_user(request.user_id)
        id_to_use = request.user_id
    else:
        await enforce_password_change_validity(
            current_password=request.current_password,
            current_password_hash=user_record.password_hash,
            new_password=request.new_password,
            new_password_confirm=request.new_password_confirm,
        )

    try:
        await change_user_password(user_id=id_to_use, new_password_hash=hash_password(request.new_password), mandate_reset=bool(request.mandate_reset))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while changing password. Please try again later.") from e

    return {"message": "Password changed successfully."}