from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserDisplayInfo(BaseModel):
    id: int
    email: EmailStr
    username: str
    profile_picture_url: str | None = None
    role: str | None = None
    joined_date: datetime
    last_login: datetime | None = None
    password_expires_at: datetime | None = None

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