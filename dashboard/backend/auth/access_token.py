from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta

from dashboard.backend.management import convert_orm_to_display_info
from dashboard.backend.models.dto_models import UserDisplayInfo, AccessTokenInfo
from dashboard.backend.db import get_user_by_id

from shared.config import LOGIN_SECRET_KEY, TOKEN_EXPIRATION_MINS, TOKEN_ENCODING_ALGORITHM

_bearer = HTTPBearer(auto_error=False)

def create_access_token(data: AccessTokenInfo):
    to_encode = data.model_dump()

    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, LOGIN_SECRET_KEY, algorithm=TOKEN_ENCODING_ALGORITHM)

    return encoded_jwt

async def get_user_from_token(token: str) -> UserDisplayInfo | None:
    try:
        payload = jwt.decode(token, LOGIN_SECRET_KEY, algorithms=[TOKEN_ENCODING_ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            return None

        user_record = await get_user_by_id(user_id)
        if user_record is None:
            return None
        
        return convert_orm_to_display_info(user_record)

    except JWTError:
        return None
    
async def verify_access_token(token: str) -> bool:
    try:
        _ = jwt.decode(token, LOGIN_SECRET_KEY, algorithms=[TOKEN_ENCODING_ALGORITHM])
        return True
    except JWTError:
        return False


async def require_valid_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> bool:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing access token")

    if not await verify_access_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    return True

async def require_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> UserDisplayInfo:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing access token")

    user = await get_user_from_token(credentials.credentials)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    return user