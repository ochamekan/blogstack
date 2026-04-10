from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.tags.models import Tag


class TagsRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def create_tag(self, new_tag: Tag) -> Tag:
        self._db.add(new_tag)
        await self._db.commit()
        await self._db.refresh(new_tag)
        return new_tag

    async def get_tags(self, q: str) -> list[Tag]:
        result = await self._db.execute(
            select(Tag).where(Tag.name.icontains(q.lower()))
        )
        tags = list(result.scalars().all())
        return tags
