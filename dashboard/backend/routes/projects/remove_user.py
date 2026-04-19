from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dashboard.backend.models import AddUserToProjectRequest
from dashboard.backend.auth import require_project_manager_user
from dashboard.backend.db import remove_user_from_project as db_remove_user_from_project

router = APIRouter(prefix="/projects", tags=["projects"])
_bearer = HTTPBearer(auto_error=False)

@router.post("/remove-user", description="Remove a user from a project")
async def remove_user_from_project(
    request: AddUserToProjectRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
):
    """
    Remove a user from a project after verifying manager permissions.

    Parameters
    ----------
    - request: Payload containing project and user identifiers.
    - credentials: Optional bearer credentials used for permission validation.

    Returns
    -------
    - A success message dictionary when membership removal completes.
    """
    await require_project_manager_user(request.project_id, credentials)

    try:
        await db_remove_user_from_project(project_id=request.project_id, user_id=request.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while removing user from project. Please try again later.") from e

    return {"message": "User removed successfully."}
