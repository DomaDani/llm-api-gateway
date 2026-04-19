from datetime import datetime
from pydantic import BaseModel

from shared.models import Status

class ProjectDisplayInfo(BaseModel):
    """DTO representing project details returned by project endpoints."""

    id: int
    name: str
    status: Status
    created_date: datetime
    modified_date: datetime | None = None

class CreateProjectRequest(BaseModel):
    """DTO for creating a new project."""

    name: str
    manager_id: int

class AddUserToProjectRequest(BaseModel):
    """DTO for adding or removing a user in a project."""

    project_id: int
    user_id: int

class ProjectDeleteRequest(BaseModel):
    """DTO for archiving a project by identifier."""

    project_id: int