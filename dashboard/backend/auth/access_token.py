from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta

from dashboard.backend.management import user_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.models import UserDisplayInformation, AccessTokenInfo
from dashboard.backend.db import get_user_by_id, is_user_administrator, is_user_project_manager

from shared.config import LOGIN_SECRET_KEY, TOKEN_EXPIRATION_MINS, TOKEN_ENCODING_ALGORITHM

_bearer = HTTPBearer(auto_error=False)

def create_access_token(data: AccessTokenInfo):
    """
    Create a JWT access token containing the user information and an expiration time.

    Parameters
    ----------

    - data: An AccessTokenInfo object containing the user ID and optionally the project ID to be included in the token payload.
        
    Returns
    -------
    - A JWT-encoded string that can be used as an access token for authenticating requests to protected endpoints.
    """
    to_encode = data.model_dump()

    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, LOGIN_SECRET_KEY, algorithm=TOKEN_ENCODING_ALGORITHM)

    return encoded_jwt

async def get_user_from_token(token: str, project_id: int | None = None) -> UserDisplayInformation | None:
    """
    Extract the user information from a JWT access token. It decodes the token, verifies its validity, and retrieves the corresponding user record from the database.

    Parameters
    ----------
    - token: The JWT access token string to be decoded and validated.
    - project_id: Optional project ID to include permissions in the information.

    Returns
    -------
    - A UserDisplayInformation object containing the user's information if the token is valid and the user exists, or None if the token is invalid or the user cannot be found.
    """
    try:
        payload = jwt.decode(token, LOGIN_SECRET_KEY, algorithms=[TOKEN_ENCODING_ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            return None

        user_record = await get_user_by_id(user_id)
        if user_record is None:
            return None
        
        return await convert_orm_to_display_info(user_record, project_id=project_id)

    except JWTError:
        return None
    
def verify_access_token(token: str) -> bool:
    """
    Verifies if the provided JWT access token is valid by attempting to decode it with the secret key and expected algorithm. It checks for the presence of the required fields and ensures that the token has not expired.

    Parameters
    ----------
    - token: The JWT access token string to be verified.

    Returns
    -------
    - True if the token is valid and can be decoded successfully, False otherwise (including if the token is expired or malformed).
    """
    try:
        _ = jwt.decode(token, LOGIN_SECRET_KEY, algorithms=[TOKEN_ENCODING_ALGORITHM])
        return True
    except JWTError:
        return False


async def require_valid_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> None:
    """
    A FastAPI dependency that checks for the presence of a valid JWT access token in the request headers. It uses the HTTPBearer security scheme to extract the token and verifies its validity. If the token is missing, invalid, or expired, it raises an HTTPException with a 401 status code.
    On failure, it raises an HTTPException with a 401 status code and an appropriate error message indicating the reason for the failure (e.g., missing token, invalid token, expired token).
    
    Parameters
    ----------
    - credentials: An optional HTTPAuthorizationCredentials object provided by the HTTPBearer security scheme, containing the access token from the request headers.
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing access token")

    if not verify_access_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

async def require_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> UserDisplayInformation:
    """
    A FastAPI dependency that retrieves the current user's information based on the provided JWT access token. It first checks for the presence of the token, then decodes and validates it to extract the user ID. It fetches the corresponding user record from the database and returns a UserDisplayInformation object containing the user's details. If any step fails (e.g., missing token, invalid token, user not found), it raises an HTTPException with a 401 status code.
    Used for endpoints that require authentication and need access to the current user's information.

    Parameters
    ----------
    - credentials: An optional HTTPAuthorizationCredentials object provided by the HTTPBearer security scheme, containing the access token from the request headers.

    Returns
    -------
    - A UserDisplayInformation object containing the authenticated user's information if the token is valid and the user exists, or raises an HTTPException if authentication fails.
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing access token")

    user = await get_user_from_token(credentials.credentials)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    return user

async def require_administrator_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> UserDisplayInformation:
    """
    A FastAPI dependency that ensures the current user is an administrator. It retrieves the user's information using the provided JWT access token and checks if the user has administrator privileges. If the user is not an administrator, it raises an HTTPException with a 403 status code. This dependency is used for endpoints that require administrator-level access.

    Parameters
    ----------
    - credentials: An optional HTTPAuthorizationCredentials object provided by the HTTPBearer security scheme, containing the access token from the request headers.

    Returns
    -------
    - A UserDisplayInformation object containing the authenticated user's information if the user is an administrator, or raises an HTTPException if the user is not an administrator or if authentication fails.
    """
    user = await require_current_user(credentials)

    if not await is_user_administrator(user.id):
        raise HTTPException(status_code=403, detail="Administrator privileges required")

    return user

async def require_project_manager_user(
    project_id: int,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> UserDisplayInformation:
    """
    A FastAPI dependency that ensures the current user has project manager privileges for a specific project. It retrieves the user's information using the provided JWT access token and checks if the user is either an administrator or a project manager for the specified project. If the user does not have the required privileges, it raises an HTTPException with a 403 status code. This dependency is used for endpoints that require project manager-level access.

    Parameters
    ----------
    - project_id: The ID of the project for which project manager privileges are required.
    - credentials: An optional HTTPAuthorizationCredentials object provided by the HTTPBearer security scheme, containing the access token from the request headers.

    Returns
    -------
    - A UserDisplayInformation object containing the authenticated user's information if the user has project manager privileges for the specified project, or raises an HTTPException if the user does not have the required privileges or if authentication fails.
    """
    user = await require_current_user(credentials)

    if await is_user_administrator(user.id):
        return user
    if not await is_user_project_manager(user.id, project_id):
        raise HTTPException(status_code=403, detail="Project manager privileges required")

    return user