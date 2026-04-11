from sqlalchemy import select

from shared.db import get_session
from shared.models import APIKey, Project, Status

async def db_key_check(api_key: str) -> APIKey:
    async with get_session() as session:
        api_fingerprint = api_key[:12]
        result = await session.execute(
            select(APIKey)
            .join(Project, APIKey.project_id == Project.id)
            .where(
                APIKey.fingerprint == api_fingerprint,
                APIKey.status == Status.ACTIVE,
                Project.status == Status.ACTIVE,
            )
        )
        key_record = result.scalars().one_or_none()
        if not key_record:
            raise ValueError("Invalid API Key")
        return key_record