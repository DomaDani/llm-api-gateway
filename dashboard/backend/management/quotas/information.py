from shared.models import Quota
from dashboard.backend.models import QuotaDisplayInformation
from dashboard.backend.db import get_limit_by_id

async def convert_orm_to_display_info(quota_orm: Quota) -> QuotaDisplayInformation:
    limit = await get_limit_by_id(limit_id=quota_orm.limit_id)

    project_name = quota_orm.project.name if quota_orm.project else "Global"
    user_specific = f"User-Specific [{quota_orm.user.username}]" if quota_orm.user else ""
    key_specific = f"Key-Specific [{quota_orm.api_key.name}]" if quota_orm.api_key else ""
    limit_name = limit.name if limit else "Unknown"
    name = f"{project_name} {user_specific} {key_specific} {limit_name}".strip()

    return QuotaDisplayInformation(
        id=quota_orm.id,
        name=name,
        project_id=quota_orm.project_id,
        user_id=quota_orm.user_id,
        key_id=quota_orm.key_id,
        limit_id=quota_orm.limit_id,
        limit_name=limit.name if limit else None,
        limit_value=quota_orm.limit_value,
        period=quota_orm.period,
        expires_at=quota_orm.expires_at,
        status=quota_orm.status,
        allocated=quota_orm.allocated,
        next_reset=quota_orm.next_reset
    )