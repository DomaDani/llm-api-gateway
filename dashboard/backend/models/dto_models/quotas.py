from datetime import datetime
from pydantic import BaseModel, model_validator

from shared.models import Status

class QuotaDisplayInformation(BaseModel):
    id: int
    name: str | None = None
    project_id: int | None = None
    user_id: int | None = None
    key_id: int | None = None
    limit_id: int
    limit_name: str
    limit_value: float | None = None
    period: str
    expires_at: datetime | None = None
    status: Status
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

class QuotaInformationRequest(BaseModel):
    project_id: int | None = None
    user_id: int | None = None
    key_id: int | None = None
    active_only: bool = False

    @model_validator(mode="after")
    def validate_request(self):
        if sum(x is not None for x in [self.project_id, self.user_id, self.key_id]) > 1:
            raise ValueError("Only one of project_id, user_id, or key_id can be provided.")
        return self

class QuotaDeleteRequest(BaseModel):
    id: int

