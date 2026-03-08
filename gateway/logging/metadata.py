import asyncio

from ..db.mock_db import mock_limit_change, mock_db_limit_check

async def mock_async_logger(metadata: dict):
    mock_limit_change(metadata["key_id"], metadata["total_tokens"]-metadata["estimated_tokens"])
    print(f"[LOGGER] New quota values: {mock_db_limit_check(metadata['key_id'])}")

    # Simulate async logging delay
    await asyncio.sleep(0.3)

    print(f"[LOGGER] Saved metadata: {metadata}")