from datetime import datetime
from pydantic import BaseModel

from shared.models import Status

class ProjectDisplayInfo(BaseModel):
    id: int
    name: str
    status: Status
    created_date: datetime
    modified_date: datetime | None = None

class CreateProjectRequest(BaseModel):
    name: str
    manager_id: int

class AddUserToProjectRequest(BaseModel):
    project_id: int
    user_id: int

class ProjectDeleteRequest(BaseModel):
    project_id: int