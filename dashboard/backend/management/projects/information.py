from shared.models import Project
from dashboard.backend.models import ProjectDisplayInfo
from dashboard.backend.db import get_project_by_name

def convert_orm_to_display_info(project_orm: Project) -> ProjectDisplayInfo:
    return ProjectDisplayInfo(
        id=project_orm.id,
        name=project_orm.name,
        status=project_orm.status,
        created_date=project_orm.created_date,
        modified_date=project_orm.modified_date
    )

async def enforce_name_availability(name: str) -> None:
    existing_project = await get_project_by_name(name)
    if existing_project is not None:
        raise ValueError("Project name is already in use.")