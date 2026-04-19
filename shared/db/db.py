from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from shared.config import SQLALCHEMY_DATABASE_URL


# Use sqlite-specific connect args when applicable.
_connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args=_connect_args, future=True)

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous context manager for obtaining a SQLAlchemy session. It creates a new session using the SessionLocal factory and yields it for use within the context. The session is automatically closed when the context is exited.

    Returns
    -------
    - AsyncSession: An asynchronous SQLAlchemy session for interacting with the database.
    """
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def get_transactional_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous context manager for obtaining a transactional SQLAlchemy session. It creates a new session using the SessionLocal factory and yields it for use within the context. The session is automatically closed when the context is exited.

    Returns
    -------
    - AsyncSession: An asynchronous transactional SQLAlchemy session for interacting with the database.
    """
    async with SessionLocal() as session:
        async with session.begin():
            yield session
