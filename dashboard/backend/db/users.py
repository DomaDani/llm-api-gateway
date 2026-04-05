from sqlalchemy import select

from shared.db import get_session
from shared.models import User

async def get_user_by_email(email: str) -> User | None:
    async with get_session() as session:
        result = await session.execute(select(User).where(User.email == email))

        user_record = result.scalars().first()

        return user_record