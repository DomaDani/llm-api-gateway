
from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserRegistrationRequest
from dashboard.backend.management.users import enforce_availability, enforce_password_strength
from dashboard.backend.auth import require_administrator_user
from dashboard.backend.db import create_user
from dashboard.backend.models import UserDisplayInfo

from shared.utils.password import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", description="Register a new user.")
async def register(request: UserRegistrationRequest, _: UserDisplayInfo = Depends(require_administrator_user)):
    await enforce_availability(email=request.email, username=request.username)

    await enforce_password_strength(request.password)

    try:
        new_user = await create_user(email=request.email, username=request.username, password_hash=hash_password(request.password), mandate_reset=request.mandate_reset)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong during registration. Please try again later.") from e

    return {"message": f"User {new_user.username} registered successfully."}