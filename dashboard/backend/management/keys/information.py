from shared.models import APIKey
from dashboard.backend.models import ApiKeyDisplayInformation


def convert_orm_to_display_info(key_orm: APIKey, api_key: str | None = None) -> ApiKeyDisplayInformation:
    return ApiKeyDisplayInformation(
        id=key_orm.id,
        project_id=key_orm.project_id,
        user_id=key_orm.user_id,
        name=key_orm.name,
        fingerprint=key_orm.fingerprint,
        api_key=api_key,
        create_date=key_orm.create_date,
        status=key_orm.status,
    )
