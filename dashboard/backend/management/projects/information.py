from shared.models import Project
from dashboard.backend.models import ProjectDisplayInfo

def convert_orm_to_display_info(project_orm: Project) -> ProjectDisplayInfo:
    return ProjectDisplayInfo(
        id=project_orm.id,
        name=project_orm.name,
        status=project_orm.status,
        created_date=project_orm.created_date,
        modified_date=project_orm.modified_date
    )