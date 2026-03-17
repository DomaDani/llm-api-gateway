import asyncio

from gateway.db import mock_limit_change, mock_db_limit_check
from shared.models.sqlalchemy.usage_log import UsageLog
from gateway.models.pydantic import UsageLogEntry
from shared.db import get_transactional_session

async def mock_async_logger(metadata: dict):
    mock_limit_change(metadata["key_id"], metadata["total_tokens"]-metadata["estimated_tokens"])
    print(f"[LOGGER] New quota values: {mock_db_limit_check(metadata['key_id'])}")

    # Simulate async logging delay
    await asyncio.sleep(0.3)

    print(f"[LOGGER] Saved metadata: {metadata}")

async def usage_logger(entry: UsageLogEntry):
    async with get_transactional_session() as session:
        # For now, this is still a mock function.
        total_tokens = entry.total_tokens or 0
        mock_limit_change(entry.key_id, total_tokens-entry.estimated_tokens)

        entry_dict = entry.model_dump()

        usage_log = UsageLog(**entry_dict)
        session.add(usage_log)

        print(f"[LOGGER] Logged usage: {entry_dict}")