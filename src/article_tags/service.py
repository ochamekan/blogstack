from sqlalchemy.ext.asyncio import AsyncSession
from src.article_tags.models import ArticleTag
from src.article_tags.repository import ArticleTagsRepository
from src.articles.exceptions import ForbiddenError
from src.articles.service import ArticlesService
from src.auth.models import User


class ArticleTagsService:
    def __init__(
        self,
        articles_service: ArticlesService,
        repo: ArticleTagsRepository,
        db: AsyncSession,
    ) -> None:
        self._articles_service: ArticlesService = articles_service
        self._repo: ArticleTagsRepository = repo
        self._db: AsyncSession = db

    async def attach_tags_to_article(
        self, article_id: str, data: list[str], user: User
    ) -> list[ArticleTag]:
        article = await self._articles_service.get_article_by_id(article_id)
        if article.author_id != user.id:
            raise ForbiddenError

        tags = await self._repo.attach_tags(article.id, data)
        await self._db.commit()

        return tags
