#!/usr/bin/env python3
import sys
from pathlib import Path
import asyncio
from sqlalchemy import inspect
import argparse

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.db import engine
from shared.models import SQLAlchemyBase

from tools.create_mock_data import create_mock_data

parser = argparse.ArgumentParser()
parser.add_argument("--reset", action="store_true", help="Drop existing tables and recreate them.")
parser.add_argument("--empty", action="store_true", help="Do not create default roles and limits.")

args = parser.parse_args()

async def main() -> None:
    """
    Connects to the database using the shared engine and checks for existing tables.
    If tables exist and --reset is not specified, it will print a message and exit. If --reset is specified, it will drop all existing tables before recreating them. After ensuring the tables are created, if --empty is not specified, it will call create_mock_data to populate the database with default roles and limits.
    """
    print("Starting database bootstrap...")
    async with engine.begin() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        if tables:
            if args.reset:
                await conn.run_sync(lambda sync_conn: SQLAlchemyBase.metadata.drop_all(bind=sync_conn))
            else:
                print("Database tables already exist. Use --reset to drop and recreate them.")
                return
        await conn.run_sync(lambda sync_conn: SQLAlchemyBase.metadata.create_all(bind=sync_conn))

    if not args.empty:
        await create_mock_data(default_only=True)
        print("Database tables created.")


if __name__ == "__main__":
    asyncio.run(main())
