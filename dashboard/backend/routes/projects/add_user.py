from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dashboard.backend.models import AddUserToProjectRequest
from dashboard.backend.auth import require_project_manager_user
from dashboard.backend.db import add_user_to_project as db_add_user_to_project

router = APIRouter(prefix="/projects", tags=["projects"])
_bearer = HTTPBearer(auto_error=False)

@router.post("/add-user", description="Add a user to a project")
async def add_user_to_project(
    request: AddUserToProjectRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
):
    await require_project_manager_user(request.project_id, credentials)

    await db_add_user_to_project(request.user_id, request.project_id)

    return {"message": f"User with added successfully."}