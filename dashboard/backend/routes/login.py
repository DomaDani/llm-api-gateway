from fastapi import APIRouter, HTTPException

from dashboard.backend.models import LoginRequest, TokenResponse
from dashboard.backend.db import get_user_by_email
from dashboard.backend.auth.password import verify_password
from dashboard.backend.auth import create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse, description="Authenticate user and return access token", tags=["auth"])
async def login(request: LoginRequest):
    user = get_user_by_email(request.email)

    if user is None or not verify_password(stored_hash=user.password_hash, provided_password=request.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password!")
    

    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return TokenResponse(access_token=access_token, token_type="bearer")