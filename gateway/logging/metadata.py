import asyncio
from sqlalchemy import select
import logging

from gateway.db import db_limit_change
from shared.models.orm_models import UsageLog, APIKey
from gateway.models.dto_models import UsageLogEntry
from shared.db import get_transactional_session

async def usage_logger(entry: UsageLogEntry, failed_upstream: bool = False):
    async with get_transactional_session() as session:

        result = await session.execute(select(APIKey).where(APIKey.id == entry.key_id).limit(1))
        api_key = result.scalar_one_or_none()
        if not api_key:
            raise ValueError(f"API key with ID {entry.key_id} not found in database.")

        total_tokens = entry.total_tokens or 0
        estimated_tokens = entry.estimated_tokens or 0
        internal_cost_estimate = entry.internal_cost_estimate or 0
        internal_cost_final = entry.internal_cost_final or 0

        await db_limit_change(
            api_key,
            update_req_count=not failed_upstream,
            change_by_tokens=total_tokens-estimated_tokens,
            change_by_price=internal_cost_final-internal_cost_estimate,
            session=session
        )

        entry_dict = entry.model_dump()

        usage_log = UsageLog(**entry_dict)
        session.add(usage_log)

        print(f"Logged usage: {entry_dict}")