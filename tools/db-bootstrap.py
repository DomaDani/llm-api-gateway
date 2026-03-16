#!/usr/bin/env python3
import sys
from pathlib import Path
from sqlalchemy import inspect

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.db import engine
from shared.models import SQLAlchemyBase

if __name__ == "__main__":
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if tables:
        answer = input(f"Database contains {len(tables)} tables, drop all and recreate? Type 'yes' to continue: ").strip().lower()
        if answer != "yes":
            print("Aborted.")
            sys.exit(1)
        SQLAlchemyBase.metadata.drop_all(bind=engine)
    SQLAlchemyBase.metadata.create_all(bind=engine)
    print("Database tables created.")
