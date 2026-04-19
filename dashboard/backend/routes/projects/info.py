from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_current_user
from dashboard.backend.management import project_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.models import ProjectDisplayInfo, UserDisplayInformation
from dashboard.backend.db import (
    get_all_projects as db_get_all_projects,
    get_projects_for_user as db_get_projects_for_user,
    is_user_administrator as db_is_user_administrator,
)

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/info", description="Get information about projects based on the user.")
async def get_project_information(
    current_user: UserDisplayInformation = Depends(require_current_user),
) -> list[ProjectDisplayInfo]:
    """
    Retrieve project information scoped to the current user role.

    Parameters
    ----------
    - current_user: Authenticated user used to determine visibility scope.

    Returns
    -------
    - A list of project display models for all projects (admin) or memberships (non-admin).
    """
    try:
        if await db_is_user_administrator(current_user.id):
            project_orms = await db_get_all_projects()
        else:
            project_orms = await db_get_projects_for_user(current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching project information. Please try again later.") from e

    return [convert_orm_to_display_info(project_orm) for project_orm in project_orms]
