from fastapi import APIRouter, Depends

from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import project_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.models import ProjectDisplayInfo
from dashboard.backend.db import get_all_projects

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/all", description="Get information about all projects")
async def get_all_projects(_: None = Depends(require_valid_access_token)) -> list[ProjectDisplayInfo]:
    project_orms = await get_all_projects()
    return [convert_orm_to_display_info(project_orm) for project_orm in project_orms]