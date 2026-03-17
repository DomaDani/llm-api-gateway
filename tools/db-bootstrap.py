#!/usr/bin/env python3
import sys
from pathlib import Path
import asyncio
from sqlalchemy import inspect

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.db import engine
from shared.models import SQLAlchemyBase


async def main() -> None:
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        if tables:
            answer = input(f"Database contains {len(tables)} tables, drop all and recreate? Type 'yes' to continue: ").strip().lower()
            if answer != "yes":
                print("Aborted.")
                sys.exit(1)
            await conn.run_sync(lambda sync_conn: SQLAlchemyBase.metadata.drop_all(bind=sync_conn))

        await conn.run_sync(lambda sync_conn: SQLAlchemyBase.metadata.create_all(bind=sync_conn))
        print("Database tables created.")


if __name__ == "__main__":
    asyncio.run(main())
