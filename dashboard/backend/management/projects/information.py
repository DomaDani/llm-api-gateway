from fastapi import HTTPException

from shared.models import Project
from dashboard.backend.models import ProjectDisplayInfo
from dashboard.backend.db import get_project_by_name, get_project_by_id, get_user_permissions_for_project, is_user_administrator

def convert_orm_to_display_info(project_orm: Project) -> ProjectDisplayInfo:
    return ProjectDisplayInfo(
        id=project_orm.id,
        name=project_orm.name,
        status=project_orm.status,
        created_date=project_orm.created_date,
        modified_date=project_orm.modified_date
    )

async def enforce_name_availability(name: str) -> None:
    existing_project = await get_project_by_name(name, active_only=False)
    if existing_project is not None:
        raise HTTPException(status_code=400, detail="Project name is already in use.")


async def enforce_existing_project(project_id: int) -> Project:
    project = await get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")

    return project

async def enforce_user_not_in_project(user_id: int, project_id: int) -> None:
    project = await get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")

    if await is_user_administrator(user_id):
        raise HTTPException(status_code=400, detail="User is already a member of the project.")
    
    permissions = await get_user_permissions_for_project(project_id, user_id)
    if permissions is not None:
        raise HTTPException(status_code=400, detail="User is already a member of the project.")
