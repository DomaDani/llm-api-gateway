from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserDisplayInformation(BaseModel):
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
    email: EmailStr
    username: str
    password: str
    mandate_reset: bool = False

class UserIdentityChangeRequest(BaseModel):
    email: EmailStr
    username: str

class UserPasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str

class UserInformationRequest(BaseModel):
    project_id: int | None = None

class UserDeleteRequest(BaseModel):
    user_id: int