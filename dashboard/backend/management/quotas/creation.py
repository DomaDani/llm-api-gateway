from fastapi import HTTPException

from dashboard.backend.db import get_limit_by_id, get_project_by_id, get_user_by_id, get_key_by_id


async def enforce_existing_limit(limit_id: int) -> None:
    """
    Ensure a quota limit type definition exists.

    Parameters
    ----------
    - limit_id: Identifier of the limit type.

    Returns
    -------
    - None.
    """
    limit = await get_limit_by_id(limit_id)
    if limit is None:
        raise HTTPException(status_code=404, detail="Limit type not found.")


async def enforce_existing_quota_target(
    project_id: int | None,
    user_id: int | None,
    key_id: int | None,
) -> None:
    """
    Ensure requested quota target entities exist.

    Parameters
    ----------
    - project_id: Optional project identifier.
    - user_id: Optional user identifier.
    - key_id: Optional API key identifier.

    Returns
    -------
    - None.
    """
    if project_id is not None:
        project = await get_project_by_id(project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found.")

    if user_id is not None:
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

    if key_id is not None:
        api_key = await get_key_by_id(key_id)
        if api_key is None:
            raise HTTPException(status_code=404, detail="API key not found.")
