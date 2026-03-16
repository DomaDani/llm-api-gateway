#!/usr/bin/env python3
import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.db import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)
try:
    tables = inspector.get_table_names()
except Exception as e:
    print(e)
    sys.exit(1)

preparer = None
try:
    preparer = engine.dialect.identifier_preparer
except Exception:
    preparer = None

with engine.connect() as conn:
    for t in tables:
        # try to quote the identifier for safety
        try:
            qname = preparer.quote(t) if preparer is not None else t
        except Exception:
            qname = t

        try:
            res = conn.execute(text(f"SELECT COUNT(*) AS cnt FROM {qname}"))
            try:
                # SQLAlchemy 1.4+: Result.scalar()
                count = res.scalar()
            except Exception:
                row = res.fetchone()
                count = row[0] if row is not None else 0
        except Exception:
            count = "?"

        print(f"{t} [{count}]")
