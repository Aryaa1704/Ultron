from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import MemoryEntry


class UserProfileStore:
    async def set_preference(
        self,
        session: AsyncSession,
        user_id: int,
        key: str,
        value: str,
    ) -> None:
        session.add(MemoryEntry(user_id=user_id, key=f"profile:{key}", value=value))
        await session.commit()

    async def get_preference(
        self,
        session: AsyncSession,
        user_id: int,
        key: str,
    ) -> str | None:
        entry = await session.scalar(
            select(MemoryEntry)
            .where(
                MemoryEntry.user_id == user_id,
                MemoryEntry.key == f"profile:{key}",
            )
            .order_by(MemoryEntry.id.desc())
        )
        return entry.value if entry else None
