from sqlalchemy.ext.asyncio import AsyncSession
from src.articles.models import Article


class ArticlesRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def create_article(self, new_article: Article) -> Article:
        self._db.add(new_article)
        await self._db.commit()
        await self._db.refresh(new_article)
        return new_article
