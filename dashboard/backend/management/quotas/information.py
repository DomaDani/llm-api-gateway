from shared.models import Quota
from dashboard.backend.models import QuotaDisplayInformation
from dashboard.backend.db import get_limit_by_id, get_user_by_id, get_key_by_id

async def convert_orm_to_display_info(quota_orm: Quota, add_name: bool = False) -> QuotaDisplayInformation:
    """
    Convert a quota ORM entity to a quota display DTO.

    Parameters
    ----------
    - quota_orm: Source quota ORM model.
    - add_name: Whether a generated human-readable name should be included.

    Returns
    -------
    - QuotaDisplayInformation mapped from ORM data.
    """
    limit = await get_limit_by_id(limit_id=quota_orm.limit_id)

    if add_name:
        project_name = quota_orm.project.name if quota_orm.project else "Global"
        user_specific = f"User-Specific [{quota_orm.user.username}]" if quota_orm.user else ""
        key_specific = f"Key-Specific [{quota_orm.api_key.name}]" if quota_orm.api_key else ""
        limit_name = limit.name if limit else "Unknown"
        name = f"{project_name} {user_specific} {key_specific} {limit_name}".strip()
    else:
        name = None

    user = await get_user_by_id(quota_orm.user_id) if quota_orm.user_id else None
    user_name = user.username if user else None

    key = await get_key_by_id(quota_orm.key_id) if quota_orm.key_id else None
    fingerprint = key.fingerprint if key else None

    return QuotaDisplayInformation(
        id=quota_orm.id,
        name=name,
        project_id=quota_orm.project_id,
        user_name=user_name,
        fingerprint=fingerprint,
        limit_id=quota_orm.limit_id,
        limit_name=limit.name if limit else None,
        limit_value=quota_orm.limit_value,
        period=quota_orm.period,
        expires_at=quota_orm.expires_at,
        status=quota_orm.status,
        allocated=quota_orm.allocated,
        next_reset=quota_orm.next_reset
    )