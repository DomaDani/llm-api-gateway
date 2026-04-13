from fastapi import APIRouter, HTTPException

from dashboard.backend.models import LoginRequest, TokenResponse, AccessTokenInfo
from dashboard.backend.db import get_user_by_email
from shared.utils import verify_password
from dashboard.backend.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse, description="Authenticate user and return access token")
async def login(request: LoginRequest):
    try:
        user = await get_user_by_email(request.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while logging in. Please try again later.") from e

    if user is None or not verify_password(stored_hash=user.password_hash, provided_password=request.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password!")

    access_token = create_access_token(data=AccessTokenInfo(user_id=user.id, sub=user.email))
    return TokenResponse(access_token=access_token, token_type="bearer")