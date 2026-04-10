from fastapi import APIRouter, Depends

from dashboard.backend.models import CreateProjectRequest, UserDisplayInformation
from dashboard.backend.auth import require_administrator_user
from dashboard.backend.management import project_enforce_availability, enforce_existing_user
from dashboard.backend.db import create_project

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/create", description="Create a new project")
async def create_project(request: CreateProjectRequest, _: UserDisplayInformation = Depends(require_administrator_user)):
    await project_enforce_availability(request.name)
    await enforce_existing_user(request.owner_id)

    project = await create_project(name=request.name, owner_id=request.owner_id)

    return {"message": f"Project '{project.name}' created successfully."}