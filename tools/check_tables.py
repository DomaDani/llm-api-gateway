#!/usr/bin/env python3
import sys
from pathlib import Path
import asyncio

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.db import engine
from sqlalchemy import inspect, text


async def main() -> None:
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

        for t in tables:
            def sync_count(sync_conn, table_name: str):
                try:
                    preparer = sync_conn.dialect.identifier_preparer
                except Exception:
                    preparer = None

                try:
                    qname = preparer.quote(table_name) if preparer is not None else table_name
                except Exception:
                    qname = table_name

                try:
                    res = sync_conn.execute(text(f"SELECT COUNT(*) AS cnt FROM {qname}"))
                    try:
                        return res.scalar()
                    except Exception:
                        row = res.fetchone()
                        return row[0] if row is not None else 0
                except Exception:
                    return "?"

            count = await conn.run_sync(sync_count, t)
            print(f"{t} [{count}]")


if __name__ == "__main__":
    asyncio.run(main())
