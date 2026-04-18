from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.claps.models import Clap


class ClapRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def create_clap(self, article_id: str, user_id: str) -> Clap:
        new_clap = Clap(article_id=article_id, user_id=user_id)
        self._db.add(new_clap)
        await self._db.commit()
        await self._db.refresh(new_clap)
        return new_clap

    async def increment_clap(self, clap_id: str) -> Clap:
        res = await self._db.execute(select(Clap).where(Clap.id == clap_id))
        clap = res.scalar_one()
        clap.count += 1
        self._db.add(clap)
        await self._db.commit()
        await self._db.refresh(clap)
        return clap

    async def get_clap(self, article_id: str, user_id: str) -> Clap | None:
        res = await self._db.execute(
            select(Clap).where(
                Clap.article_id == article_id and Clap.user_id == user_id
            )
        )
        clap = res.scalar_one_or_none()
        return clap
