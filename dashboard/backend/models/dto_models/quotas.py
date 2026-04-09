from datetime import datetime
from pydantic import BaseModel

class QuotaDisplayInfo(BaseModel):
    id: int
    project_id: int | None = None
    user_id: int | None = None
    key_id: int | None = None
    limit_id: int
    limit_name: str
    limit_value: float | None = None
    period: str
    expires_at: datetime | None = None
    status: str
    allocated: float
    next_reset: datetime

class QuotaCreateRequest(BaseModel):
    project_id: int | None = None
    user_id: int | None = None
    key_id: int | None = None
    limit_id: int
    limit_value: float | None = None
    period: str
    expires_at: datetime | None = None

class QuotaInfoRequest(BaseModel):
    project_id: int | None = None
    user_id: int | None = None
    key_id: int | None = None

class QuotaDeleteRequest(BaseModel):
    id: int

