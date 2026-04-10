from datetime import datetime
from pydantic import BaseModel

from shared.models import Status

class CreateApiKeyRequest(BaseModel):
    project_id: int
    user_id: int
    name: str


class ApiKeyDeleteRequest(BaseModel):
    key_id: int


class ApiKeyDisplayInformation(BaseModel):
    id: int
    project_id: int
    user_id: int
    name: str
    fingerprint: str
    api_key: str | None = None
    create_date: datetime
    status: Status
