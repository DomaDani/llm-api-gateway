from fastapi import APIRouter, Depends, HTTPException

from dashboard.backend.auth import require_administrator_user
from dashboard.backend.db import create_key as db_create_key, is_user_project_member
from dashboard.backend.management import generate_api_key, project_enforce_existing_project, user_enforce_existing_user
from dashboard.backend.models import ApiKeyDisplayInformation, CreateApiKeyRequest, UserDisplayInformation
from shared.config import FINGERPRINT_LENGTH
from shared.utils import hash_key

router = APIRouter(prefix="/keys", tags=["keys"])


@router.post("/create", response_model=ApiKeyDisplayInformation, description="Create a new API key.")
async def create_api_key(
    request: CreateApiKeyRequest,
    _: UserDisplayInformation = Depends(require_administrator_user),
):
    try:
        await project_enforce_existing_project(request.project_id)
        await user_enforce_existing_user(request.user_id)

        if not await is_user_project_member(request.project_id, request.user_id):
            raise HTTPException(status_code=400, detail="User is not a member of this project.")

        api_key_value = generate_api_key(64)
        fingerprint = api_key_value[:FINGERPRINT_LENGTH]
        created_key = await db_create_key(
            project_id=request.project_id,
            user_id=request.user_id,
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

    return ApiKeyDisplayInformation(
        id=created_key.id,
        project_id=created_key.project_id,
        user_id=created_key.user_id,
        name=created_key.name,
        fingerprint=created_key.fingerprint,
        api_key=api_key_value,
        create_date=created_key.create_date,
        status=created_key.status,
    )
