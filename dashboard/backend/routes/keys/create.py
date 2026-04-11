from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_current_user
from dashboard.backend.db import create_key as db_create_key, is_user_project_member, is_user_administrator
from dashboard.backend.management import (
    generate_api_key,
    key_convert_orm_to_display_info as convert_orm_to_display_info,
    project_enforce_existing_project,
)
from dashboard.backend.models import ApiKeyDisplayInformation, CreateApiKeyRequest, UserDisplayInformation
from shared.config import FINGERPRINT_LENGTH
from shared.utils import hash_key

router = APIRouter(prefix="/keys", tags=["keys"])


@router.post("/create", response_model=ApiKeyDisplayInformation, description="Create a new API key.")
async def create_api_key(
    request: CreateApiKeyRequest,
    current_user: UserDisplayInformation = Depends(require_current_user),
):
    try:
        await project_enforce_existing_project(request.project_id)

        if not await is_user_project_member(request.project_id, current_user.id):
            if not await is_user_administrator(current_user.id):
                raise HTTPException(status_code=400, detail="User is not a member of this project.")

        api_key_value = generate_api_key(64)
        fingerprint = api_key_value[:FINGERPRINT_LENGTH]
        created_key = await db_create_key(
            project_id=request.project_id,
            user_id=current_user.id,
            name=request.name,
            fingerprint=fingerprint,
            key_hash=hash_key(api_key_value),
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while creating API key. Please try again later.") from e

    return convert_orm_to_display_info(created_key, api_key=api_key_value, username=current_user.username)
