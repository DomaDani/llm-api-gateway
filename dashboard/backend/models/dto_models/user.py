from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserDisplayInformation(BaseModel):
    """DTO representing user information returned by dashboard endpoints."""

    id: int
    email: EmailStr
    username: str
    profile_picture_url: str | None = None
    role: str | None = None
    joined_date: datetime
    last_login: datetime | None = None
    password_expires_at: datetime | None = None
    is_admin: bool = False
    is_project_manager: bool = False
    is_password_expired: bool = False

class UserRegistrationRequest(BaseModel):
    """DTO for registering a new user."""

    email: EmailStr
    username: str
    password: str
    mandate_reset: bool = False

class UserIdentityChangeRequest(BaseModel):
    """DTO for changing a user's email and username."""

    email: EmailStr
    username: str

class UserPasswordChangeRequest(BaseModel):
    """DTO for changing a user's password."""

    current_password: str | None = None
    user_id: int | None = None
    new_password: str
    new_password_confirm: str
    mandate_reset: bool | None = False

class UserInformationRequest(BaseModel):
    """DTO for requesting user information with optional project scope."""

    project_id: int | None = None

class UserDeleteRequest(BaseModel):
    """DTO for deleting a user by identifier."""

    user_id: int