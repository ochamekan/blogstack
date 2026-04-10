from math import ceil
from typing import cast
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.articles.models import Article


class ArticlesRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def get_articles(self, page: int, limit: int) -> tuple[list[Article], int]:
        articles = await self._db.execute(
            select(Article)
            .order_by(Article.created_at.desc())
            .offset(limit * page - limit)
            .limit(limit)
        )
        total_articles = await self._db.execute(
            select(func.count()).select_from(Article)
        )
        total_articles = cast(int, total_articles.scalar())

        return (list(articles.scalars().all()), ceil(total_articles / limit))

    async def create_article(self, new_article: Article) -> Article:
        self._db.add(new_article)
        await self._db.commit()
        await self._db.refresh(new_article)
        return new_article

    async def get_article_by_slug(self, slug: str) -> Article | None:
        article = await self._db.execute(select(Article).where(Article.slug == slug))
        return article.scalar_one_or_none()

    async def update_article(self, updated_article: Article) -> Article:
        self._db.add(updated_article)
        await self._db.commit()
        await self._db.refresh(updated_article)
        return updated_article
