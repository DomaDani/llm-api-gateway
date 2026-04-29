from fastapi import HTTPException

from dashboard.backend.db import get_quota_by_id, is_user_administrator, is_user_project_manager


async def enforce_quota_creation_permission(
    current_user_id: int,
    project_id: int | None,
    user_id: int | None,
    key_id: int | None,
) -> None:
    """
    Ensure the current user can create a quota for the requested scope.

    Parameters
    ----------
    current_user_id : int
        Identifier of the requesting user.
    project_id : int | None
        Optional project identifier for scoped quotas.
    user_id : int | None
        Optional user identifier target.
    key_id : int | None
        Optional API key identifier target.

    Returns
    -------
    None
        None.
    """
    is_admin = await is_user_administrator(current_user_id)

    if project_id is None:
        if not is_admin:
            raise HTTPException(status_code=403, detail="Administrator privileges required for global quotas.")
        return

    if not is_admin and not await is_user_project_manager(user_id=current_user_id, project_id=project_id):
        raise HTTPException(status_code=403, detail="Project manager privileges required for project quotas.")


async def enforce_quota_deletion_permission(current_user_id: int, quota_id: int) -> None:
    """
    Ensure the current user can delete the target quota.

    Parameters
    ----------
    current_user_id : int
        Identifier of the requesting user.
    quota_id : int
        Identifier of the quota to delete.

    Returns
    -------
    None
        None.
    """
    if await is_user_administrator(current_user_id):
        return

    quota = await get_quota_by_id(quota_id)
    if quota is None:
        raise HTTPException(status_code=404, detail="Quota not found.")

    effective_project_id = quota.project_id or (quota.api_key.project_id if quota.api_key is not None else None)

    if effective_project_id is None:
        raise HTTPException(status_code=403, detail="Only administrators can delete global quotas.")

    if not await is_user_project_manager(user_id=current_user_id, project_id=effective_project_id):
        raise HTTPException(status_code=403, detail="Project manager privileges required for deleting this quota.")
