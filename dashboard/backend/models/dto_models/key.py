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
