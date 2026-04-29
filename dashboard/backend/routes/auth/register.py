
from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserRegistrationRequest
from dashboard.backend.management import user_enforce_availability, enforce_password_strength
from dashboard.backend.auth import require_administrator_user
from dashboard.backend.db import create_user
from dashboard.backend.models import UserDisplayInformation

from shared.utils import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", description="Register a new user.")
async def register(request: UserRegistrationRequest, _: UserDisplayInformation = Depends(require_administrator_user)):
    """
    Registers a new user with the provided information.
    This endpoint is protected and requires the requester to be an authenticated administrator user.

    Parameters
    ----------
    request : UserRegistrationRequest
        A UserRegistrationRequest object containing the new user's email, username, password, and mandate_reset flag.
    _ : UserDisplayInformation
        An unused UserDisplayInformation object injected by the require_administrator_user dependency to enforce admin permissions.

    Returns
    -------
    dict
        A dictionary containing a success message with the new user's username if registration is successful.
    """
    await user_enforce_availability(email=request.email, username=request.username)

    await enforce_password_strength(request.password)

    try:
        new_user = await create_user(email=request.email, username=request.username, password_hash=hash_password(request.password), mandate_reset=request.mandate_reset)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong during registration. Please try again later.") from e

    return {"message": f"User {new_user.username} registered successfully."}