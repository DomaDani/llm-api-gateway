from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import project_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.models import ProjectDisplayInfo
from dashboard.backend.db import get_all_projects as db_get_all_projects

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/all", description="Get information about all projects")
async def get_all_projects(_: None = Depends(require_valid_access_token)) -> list[ProjectDisplayInfo]:
    """
    Retrieve all visible projects in the system.

    Parameters
    ----------
    _ : None
        Token validation dependency output, unused in function body.

    Returns
    -------
    list[ProjectDisplayInfo]
        A list of project display models.
    """
    try:
        project_orms = await db_get_all_projects()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching projects. Please try again later.") from e

    return [convert_orm_to_display_info(project_orm) for project_orm in project_orms]