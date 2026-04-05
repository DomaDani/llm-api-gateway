from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserDisplayInfo(BaseModel):
    id: int
    email: EmailStr
    username: str
    profile_picture_url: str | None = None
    joined_date: datetime
    last_login: datetime | None = None
    password_expires_at: datetime | None = None