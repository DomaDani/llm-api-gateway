
from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserRegistrationRequest
from dashboard.backend.management.users import enforce_availability, enforce_password_strength
from dashboard.backend.auth import hash_password, require_valid_access_token
from dashboard.backend.db import create_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", description="Register a new user.")
async def register(request: UserRegistrationRequest, _: bool = Depends(require_valid_access_token)):
    await enforce_availability(email=request.email, username=request.username)

    await enforce_password_strength(request.password)

    try:
        new_user = await create_user(email=request.email, username=request.username, password_hash=hash_password(request.password))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong during registration. Please try again later.") from e

    return {"message": f"User {new_user.username} registered successfully."}