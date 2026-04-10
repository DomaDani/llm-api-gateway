from fastapi import HTTPException

from dashboard.backend.db import get_key_by_id, is_user_administrator, is_user_project_manager, is_user_project_member


async def enforce_quota_creation_permission(
    current_user_id: int,
    project_id: int | None,
    user_id: int | None,
    key_id: int | None,
) -> None:
    is_admin = await is_user_administrator(current_user_id)

    if project_id is None:
        if not is_admin:
            raise HTTPException(status_code=403, detail="Administrator privileges required for global quotas.")
        return

    if not is_admin and not await is_user_project_manager(user_id=current_user_id, project_id=project_id):
        raise HTTPException(status_code=403, detail="Project manager privileges required for project quotas.")

    if user_id is not None and not await is_user_project_member(project_id=project_id, user_id=user_id):
        raise HTTPException(status_code=400, detail="Target user must be a member of the specified project.")

    if key_id is not None:
        api_key = await get_key_by_id(key_id)
        if api_key is not None and api_key.project_id != project_id:
            raise HTTPException(status_code=400, detail="Target API key must belong to the specified project.")
