from fastapi import APIRouter, Depends

from dashboard.backend.models import UserDisplayInfo, UserInformationRequest
from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import user_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.db import get_all_users, get_users_by_project

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/info", response_model=UserDisplayInfo, description="Get specific information about users either globally or per project")
async def get_user_information(request: UserInformationRequest, _: UserDisplayInfo = Depends(require_valid_access_token)) -> UserDisplayInfo:
    
    if request.project_id is not None:
        user_orms = await get_users_by_project(request.project_id)
    else:   
        user_orms = await get_all_users()

    return [await convert_orm_to_display_info(user_orm, include_role=True, project_id=request.project_id) for user_orm in user_orms]