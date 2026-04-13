from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dashboard.backend.models import AddUserToProjectRequest
from dashboard.backend.auth import require_project_manager_user
from dashboard.backend.db import add_user_to_project as db_add_user_to_project
from dashboard.backend.management import project_enforce_user_not_in_project

router = APIRouter(prefix="/projects", tags=["projects"])
_bearer = HTTPBearer(auto_error=False)

@router.post("/add-user", description="Add a user to a project")
async def add_user_to_project(
    request: AddUserToProjectRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
):
    await require_project_manager_user(request.project_id, credentials)
    await project_enforce_user_not_in_project(request.user_id, request.project_id)

    try:
        await db_add_user_to_project(request.project_id, request.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while adding user to project. Please try again later.") from e

    return {"message": f"User with added successfully."}