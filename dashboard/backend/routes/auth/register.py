
from fastapi import APIRouter

from dashboard.backend.models import UserRegistrationRequest
from dashboard.backend.management.users import enforce_availability
from dashboard.backend.db import create_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", description="Register a new user.")
async def register(request: UserRegistrationRequest):
    await enforce_availability(email=request.email, username=request.username)

    new_user = await create_user(email=request.email, username=request.username, password_hash=request.password)

    return {"message": f"User {new_user.username} registered successfully."}