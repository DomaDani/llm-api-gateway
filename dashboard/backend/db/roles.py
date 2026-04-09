from sqlalchemy import select

from shared.db import get_session
from shared.models import Role

async def get_role_by_name(role_name: str, session = None) -> Role | None:
    if session is None:
        async with get_session() as session:
            return await get_role_by_name(role_name=role_name, session=session)

    result = await session.execute(select(Role).where(Role.name == role_name))
    return result.scalars().first()