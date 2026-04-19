from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """DTO for user login credentials."""

    email: EmailStr
    password: str

class AccessTokenInfo(BaseModel):
    """DTO payload stored in generated access tokens."""

    sub: EmailStr
    user_id: int

class TokenResponse(BaseModel):
    """DTO returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"