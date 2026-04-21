from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.models import UserDisplayInformation, UserInformationRequest
from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.management import user_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.db import get_all_users, get_users_by_project

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/info", response_model=list[UserDisplayInformation], description="Get specific information about users either globally or per project")
async def get_user_information(request: UserInformationRequest = Depends(), _: UserDisplayInformation = Depends(require_valid_access_token)) -> list[UserDisplayInformation]:
    """
    Retrieve user information globally or filtered by project membership.

    Parameters
    ----------
    - request: Query payload containing optional project scope.
    - _: Token validation dependency output, unused in function body.

    Returns
    -------
    - A list of user display models with optional role context.
    """
    try:
        if request.project_id is not None:
            user_orms = await get_users_by_project(request.project_id)
        else:
            user_orms = await get_all_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching user information. Please try again later.") from e

    user_infos: list[UserDisplayInformation] = []
    for user_orm in user_orms:
        try:
            user_infos.append(await convert_orm_to_display_info(user_orm, include_role=True, project_id=request.project_id))
        except ValueError:
            continue

    return user_infos