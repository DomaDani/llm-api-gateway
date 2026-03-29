import asyncio
from sqlalchemy import select
import logging

from gateway.db import db_limit_change
from shared.models.orm_models import UsageLog, APIKey
from gateway.models.dto_models import UsageLogEntry
from shared.db import get_transactional_session

logger = logging.getLogger("gateway.logging.metadata")

async def usage_logger(entry: UsageLogEntry):
    async with get_transactional_session() as session:

        result = await session.execute(select(APIKey).where(APIKey.id == entry.key_id).limit(1))
        api_key = result.scalar_one_or_none()
        if not api_key:
            raise ValueError(f"API key with ID {entry.key_id} not found in database.")

        total_tokens = entry.total_tokens or 0
        await db_limit_change(api_key, total_tokens-entry.estimated_tokens, session=session)

        entry_dict = entry.model_dump()

        usage_log = UsageLog(**entry_dict)
        session.add(usage_log)

        logger.info(f"Logged usage: {entry_dict}")