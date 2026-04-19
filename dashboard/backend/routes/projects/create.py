from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import CreateProjectRequest, UserDisplayInformation
from dashboard.backend.auth import require_administrator_user
from dashboard.backend.management import project_enforce_availability, user_enforce_existing_user
from dashboard.backend.db import create_project as db_create_project

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/create", description="Create a new project")
async def create_project(request: CreateProjectRequest, _: UserDisplayInformation = Depends(require_administrator_user)):
    """
    Create a new project and assign its initial manager.

    Parameters
    ----------
    - request: Project creation payload including name and manager user identifier.
    - _: Administrator authorization dependency output, unused in function body.

    Returns
    -------
    - A success message dictionary containing the created project name.
    """
    await project_enforce_availability(request.name)
    await user_enforce_existing_user(request.manager_id)

    try:
        project = await db_create_project(name=request.name, manager_id=request.manager_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while creating project. Please try again later.") from e

    return {"message": f"Project '{project.name}' created successfully."}