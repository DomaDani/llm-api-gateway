from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta

from dashboard.backend.models.dto_models import UserDisplayInfo
from dashboard.backend.db.users import get_user_by_email

from shared.config import LOGIN_SECRET_KEY, TOKEN_EXPIRATION_MINS, TOKEN_ENCODING_ALGORITHM

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, LOGIN_SECRET_KEY, algorithm=TOKEN_ENCODING_ALGORITHM)

    return encoded_jwt

async def get_user_from_token(token: str) -> UserDisplayInfo | None:
    try:
        payload = jwt.decode(token, LOGIN_SECRET_KEY, algorithms=[TOKEN_ENCODING_ALGORITHM])
        user_id: int = payload.get("user_id")
        email: str = payload.get("sub")

        if user_id is None or email is None:
            return None

        user_record = await get_user_by_email(email)

        if user_record is None or user_record.id != user_id:
            return None
        
        return UserDisplayInfo(
            id=user_record.id,
            email=user_record.email,
            username=user_record.username,
            profile_picture_url=user_record.profile_picture_url,
            joined_date=user_record.joined_date,
            last_login=user_record.last_login,
            password_expires_at=user_record.password_expires_at
        )

    except JWTError:
        return None