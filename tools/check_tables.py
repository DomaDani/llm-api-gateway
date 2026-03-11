#!/usr/bin/env python3
import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.db import engine
from sqlalchemy import inspect

inspector = inspect(engine)
try:
    tables = inspector.get_table_names()
except Exception as e:
    print(e)
    sys.exit(1)

for t in tables:
    print(t)
