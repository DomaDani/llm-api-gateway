from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AccessTokenInfo(BaseModel):
    sub: EmailStr
    user_id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"