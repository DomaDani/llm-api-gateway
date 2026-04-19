from shared.models import APIKey
from dashboard.backend.models import ApiKeyDisplayInformation


def convert_orm_to_display_info(
    key_orm: APIKey,
    api_key: str | None = None,
    username: str | None = None,
) -> ApiKeyDisplayInformation:
    """
    Convert an API key ORM entity to its dashboard DTO representation.

    Parameters
    ----------
    - key_orm: Source API key ORM model.
    - api_key: Optional raw API key value to include in the DTO.
    - username: Optional username override for display.

    Returns
    -------
    - ApiKeyDisplayInformation built from ORM data.
    """
    return ApiKeyDisplayInformation(
        id=key_orm.id,
        project_id=key_orm.project_id,
        user_id=key_orm.user_id,
        username=username if username is not None else (key_orm.user.username if key_orm.user else None),
        name=key_orm.name,
        fingerprint=key_orm.fingerprint,
        api_key=api_key,
        create_date=key_orm.create_date,
        status=key_orm.status,
    )
