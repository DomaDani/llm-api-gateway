from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from dashboard.backend.auth import require_project_manager_user
from dashboard.backend.db import delete_project as db_delete_project
from dashboard.backend.models import ProjectDeleteRequest

router = APIRouter(prefix="/projects", tags=["projects"])
_bearer = HTTPBearer(auto_error=False)

@router.delete("/delete", description="Archive a project by id")
async def delete_project(
    request: ProjectDeleteRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
):
    """
    Archive an existing project after verifying manager permissions.

    Parameters
    ----------
    - request: Payload containing the project identifier to archive.
    - credentials: Optional bearer credentials used for permission validation.

    Returns
    -------
    - A success message dictionary when archival completes.
    """
    await require_project_manager_user(request.project_id, credentials)

    try:
        await db_delete_project(project_id=request.project_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while deleting project. Please try again later.") from e

    return {"message": "Project archived successfully."}
