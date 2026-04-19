from fastapi import HTTPException

from dashboard.backend.db import get_key_ownership, is_user_project_manager, is_user_administrator


async def enforce_key_deletion_permission(current_user_id: int, key_id: int) -> None:
    """
    Ensure the current user is allowed to delete the target API key.

    Parameters
    ----------
    - current_user_id: Identifier of the user attempting deletion.
    - key_id: Identifier of the API key to delete.
    """
    if await is_user_administrator(current_user_id):
        return
    project, user = await get_key_ownership(key_id=key_id)

    is_owner = current_user_id == user.id
    is_project_manager = await is_user_project_manager(user_id=current_user_id, project_id=project.id)
    if not is_owner and not is_project_manager:
        raise HTTPException(status_code=403, detail="You can only delete your own API keys unless you are a project manager.")
