from sqlalchemy.ext.asyncio import AsyncSession
from src.article_tags.models import ArticleTag


class ArticleTagsRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def attach_tags(
        self, article_id: str, tag_ids: list[str]
    ) -> list[ArticleTag]:
        tags = [ArticleTag(tag_id=id, article_id=article_id) for id in tag_ids]
        self._db.add_all(tags)
        await self._db.commit()
        return tags
