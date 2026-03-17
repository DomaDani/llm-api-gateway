from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from shared.config import SQLALCHEMY_DATABASE_URL


# Use sqlite-specific connect args when applicable.
_connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args=_connect_args, future=True)

AsyncSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_transactional_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
