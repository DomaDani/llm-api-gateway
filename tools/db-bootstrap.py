#!/usr/bin/env python3

# Create the database tables based on the SQLAlchemy models.
import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.db import engine
from shared.models import SQLAlchemyBase

if __name__ == "__main__":
    SQLAlchemyBase.metadata.create_all(bind=engine)
    print("Database tables created.")
