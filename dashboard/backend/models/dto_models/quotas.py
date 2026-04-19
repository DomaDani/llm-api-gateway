from datetime import datetime
from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError

from shared.models import Status, Period

class QuotaDisplayInformation(BaseModel):
    """DTO representing quota information returned by dashboard endpoints."""

    id: int
    name: str | None = None
    project_id: int | None = None
    user_name: str | None = None
    fingerprint: str | None = None
    limit_id: int
    limit_name: str
    limit_value: float | None = None
    period: str
    expires_at: datetime | None = None
    status: Status
    allocated: float
    next_reset: datetime

class QuotaCreateRequest(BaseModel):
    """DTO for creating a quota for a project, user, or API key."""

    project_id: int | None = None
    user_id: int | None = None
    key_id: int | None = None
    limit_id: int
    limit_value: float | None = None
    period: Period
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def validate_request(self):
        if sum(x is not None for x in [self.user_id, self.key_id]) > 1:
            raise PydanticCustomError(
                "invalid_combination",
                "Only one of user_id, or key_id can be provided."
            )
        return self

class QuotaInformationRequest(BaseModel):
    """DTO for querying quotas by optional scope and filter flags."""

    project_id: int | None = None
    user_id: int | None = None
    key_id: int | None = None
    active_only: bool = False
    include_inherited: bool = True

    @model_validator(mode="after")
    def validate_request(self):
        if sum(x is not None for x in [self.project_id, self.user_id, self.key_id]) > 1:
            raise PydanticCustomError(
                "invalid_combination",
                "Only one of project_id, user_id, or key_id can be provided."
            )
        return self

class QuotaDeleteRequest(BaseModel):
    """DTO for deleting a quota by identifier."""

    id: int


class LimitTypeDisplayInformation(BaseModel):
    """DTO representing an available quota limit type."""

    id: int
    name: str
    description: str


class PeriodDisplayInformation(BaseModel):
    """DTO representing a supported quota period value."""

    name: str

