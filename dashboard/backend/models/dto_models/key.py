from datetime import datetime
from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError

from shared.models import Status

class CreateApiKeyRequest(BaseModel):
    """DTO for creating a new API key in a project."""

    project_id: int
    name: str


class ApiKeyDeleteRequest(BaseModel):
    """DTO for deleting or archiving an API key by identifier."""

    key_id: int


class KeyInformationRequest(BaseModel):
    """DTO for querying API keys by project or user scope."""
    project_id: int | None = None
    user_id: int | None = None

    @model_validator(mode="after")
    def validate_request(self):
        if sum(x is not None for x in [self.project_id, self.user_id]) != 1:
            raise PydanticCustomError(
                "invalid_combination",
                "Exactly one of project_id or user_id must be provided."
                )
        return self


class ApiKeyDisplayInformation(BaseModel):
    """DTO representing API key information returned to clients."""

    id: int
    project_id: int
    user_id: int
    username: str | None = None
    name: str
    fingerprint: str
    api_key: str | None = None
    create_date: datetime
    status: Status
