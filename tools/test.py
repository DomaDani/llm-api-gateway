#!/usr/bin/env python3
import sys
from pathlib import Path
import argparse
sys.path.insert(0, str(Path('.').resolve()))

import asyncio
from sqlalchemy import text, inspect
from shared.config import SQLALCHEMY_DATABASE_URL
from shared.models import SQLAlchemyBase
from shared.db import engine

parser = argparse.ArgumentParser()
parser.add_argument("--recreate", action="store_true", help="Run drop_all() then create_all() (destructive).")
args = parser.parse_args()

async def main():
    print("SQLALCHEMY_DATABASE_URL:", SQLALCHEMY_DATABASE_URL)
    async with engine.connect() as conn:
        print("\n-- PG search_path --")
        try:
            rows = await conn.execute(text("SHOW search_path"))
            print(rows.scalar())
        except Exception as e:
            print("SHOW search_path failed:", e)

        print("\n-- information_schema BEFORE --")
        rows = await conn.run_sync(lambda sync_conn: sync_conn.execute(text(
            "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema') ORDER BY table_schema, table_name"
        )))
        for r in rows:
            print(r)

        print("\n-- inspect.get_table_names() BEFORE --")
        names = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        print(names)

        print("\n-- SQLAlchemy metadata BEFORE --")
        for t in SQLAlchemyBase.metadata.sorted_tables:
            print((t.schema or "public", t.name))

        if args.recreate:
            print("\nCalling metadata.drop_all() then create_all() (recreate)...")
            try:
                await conn.run_sync(lambda sync_conn: SQLAlchemyBase.metadata.drop_all(bind=sync_conn))
                await conn.run_sync(lambda sync_conn: SQLAlchemyBase.metadata.create_all(bind=sync_conn))
                print("recreate completed without exception.")
            except Exception as e:
                print("recreate raised:", repr(e))

        print("\n-- information_schema AFTER --")
        rows = await conn.run_sync(lambda sync_conn: sync_conn.execute(text(
            "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema') ORDER BY table_schema, table_name"
        )))
        for r in rows:
            print(r)

        print("\n-- inspect.get_table_names() AFTER --")
        names = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        print(names)

        print("\n-- SQLAlchemy metadata AFTER --")
        for t in SQLAlchemyBase.metadata.sorted_tables:
            print((t.schema or "public", t.name))

if __name__ == "__main__":
    asyncio.run(main())