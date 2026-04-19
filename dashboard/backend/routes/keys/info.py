from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_valid_access_token
from dashboard.backend.db import get_keys_for_project, get_keys_for_user
from dashboard.backend.management import key_convert_orm_to_display_info as convert_orm_to_display_info
from dashboard.backend.models import ApiKeyDisplayInformation, KeyInformationRequest

router = APIRouter(prefix="/keys", tags=["keys"])


@router.get("/info", response_model=list[ApiKeyDisplayInformation], description="Get API keys for either a project or a user.")
async def get_key_information(
    request: KeyInformationRequest = Depends(),
    _: None = Depends(require_valid_access_token),
) -> list[ApiKeyDisplayInformation]:
    """
    Retrieve API keys scoped either to a project or to a specific user.

    Parameters
    ----------
    - request: Query parameters selecting project or user scope.
    - _: Token validation dependency output, unused in function body.

    Returns
    -------
    - A list of API key display models matching the requested scope.
    """
    try:
        if request.project_id is not None:
            key_orms = await get_keys_for_project(request.project_id)
        else:
            key_orms = await get_keys_for_user(request.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching API keys. Please try again later.") from e

    return [convert_orm_to_display_info(key_orm) for key_orm in key_orms]
