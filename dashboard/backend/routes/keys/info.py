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
    Retrieve API keys scoped either to a project or to a specific user or a specified user's keys in a project.

    Parameters
    ----------
    request : KeyInformationRequest
        Query parameters selecting project or user scope.
    _ : None
        Token validation dependency output, unused in function body.

    Returns
    -------
    list[ApiKeyDisplayInformation]
        A list of API key display models matching the requested scope.
    """
    try:
        if request.user_id is None and request.project_id is not None:
            key_orms = await get_keys_for_project(request.project_id)
        else:
            key_orms = await get_keys_for_user(user_id = request.user_id, project_id = request.project_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        print(f"Error fetching API keys: {e}")
        raise HTTPException(status_code=400, detail="Something went wrong while fetching API keys. Please try again later.") from e

    return [convert_orm_to_display_info(key_orm) for key_orm in key_orms]
