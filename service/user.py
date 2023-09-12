from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from models.models import user


async def get_user_by_tg_id(
    session: AsyncSession,
    telegram_id: int,
):
    query = select(user).where(user.telegram_id == telegram_id)

    result = await session.execute(query)

    return result.scalars().first()
