from sqlalchemy import select

from shared.db import get_session
from shared.models import APIKey, Project, Status

async def db_key_check(api_key: str, session=None) -> APIKey:
    """
    Check if the provided API key is valid and associated with an active project.
    If a session is provided, it uses that session; otherwise, it creates a new session for the query.
    
    Parameters
    ----------
    - api_key: The API key to check.
    - session: An optional SQLAlchemy session to use for the database query. If None, a new session will be created.

    Returns
    -------
    - APIKey: The API key record if it is valid and associated with an active project.
    """
    if session is None:
        async with get_session() as session:
            return await db_key_check(api_key, session=session)

    api_fingerprint = api_key[:12]
    result = await session.execute(
    select(APIKey)
    .join(Project, APIKey.project_id == Project.id)
    .where(
            APIKey.fingerprint == api_fingerprint,
            Project.status == Status.ACTIVE,
        )
    )
    key_record = result.scalars().one_or_none()
    if not key_record:
        raise ValueError("Invalid API Key")
    return key_record