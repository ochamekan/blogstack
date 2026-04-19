from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.claps.models import Clap


class ClapRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def get_total_claps(self, article_id: str) -> int:
        total = await self._db.execute(
            select(func.sum(Clap.count)).where(Clap.article_id == article_id)
        )
        return total.scalar() or 0

    async def create_clap(self, article_id: str, user_id: str) -> int:
        new_clap = Clap(article_id=article_id, user_id=user_id)
        self._db.add(new_clap)
        await self._db.commit()
        await self._db.refresh(new_clap)

        total = await self.get_total_claps(article_id)
        return total

    async def increment_clap(self, clap_id: str, article_id: str) -> int:
        res = await self._db.execute(select(Clap).where(Clap.id == clap_id))
        clap = res.scalar_one()
        if clap.count < 50:
            clap.count += 1
            await self._db.commit()

        total = await self.get_total_claps(article_id)
        return total

    async def get_clap(self, article_id: str, user_id: str) -> Clap | None:
        res = await self._db.execute(
            select(Clap).where(Clap.article_id == article_id, Clap.user_id == user_id)
        )
        return res.scalar_one_or_none()

    async def delete_claps(
        self,
        article_id: str,
        user_id: str,
    ) -> int:
        res = await self._db.execute(
            select(Clap).where(Clap.article_id == article_id, Clap.user_id == user_id)
        )
        clap = res.scalar_one_or_none()
        if clap:
            await self._db.delete(clap)
            await self._db.commit()

        total = await self.get_total_claps(article_id)
        return total
