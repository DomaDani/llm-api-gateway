import asyncio
from sqlalchemy import select

from gateway.db import db_limit_change
from shared.models.sqlalchemy import UsageLog, ApiKey
from gateway.models.pydantic import UsageLogEntry
from shared.db import get_transactional_session

async def usage_logger(entry: UsageLogEntry):
    async with get_transactional_session() as session:

        result = await session.execute(select(ApiKey).where(ApiKey.id == entry.api_key.id).limit(1))
        api_key = result.scalar_one_or_none()
        if not api_key:
            raise ValueError(f"API key with ID {entry.api_key.id} not found in database.")

        total_tokens = entry.total_tokens or 0
        db_limit_change(api_key, total_tokens-entry.estimated_tokens, session=session)

        entry_dict = entry.model_dump()

        usage_log = UsageLog(**entry_dict)
        session.add(usage_log)

        print(f"[LOGGER] Logged usage: {entry_dict}")