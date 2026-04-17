from sqlalchemy.exc import IntegrityError
from src.article_tags.exceptions import DuplicateOrMissingTagError
from src.article_tags.repository import ArticleTagsRepository
from src.article_tags.schemas import ArticleTagDTO
from src.articles.exceptions import ArticleNotFoundError, ForbiddenError
from src.articles.repository import ArticlesRepository
from src.auth.models import User


class ArticleTagsService:
    def __init__(
        self,
        articles_repo: ArticlesRepository,
        repo: ArticleTagsRepository,
    ) -> None:
        self._articles_repo: ArticlesRepository = articles_repo
        self._repo: ArticleTagsRepository = repo

    async def attach_tags_to_article(
        self, article_id: str, data: list[str], user: User
    ) -> list[ArticleTagDTO]:
        article = await self._articles_repo.get_article_by_id(article_id)
        if not article:
            raise ArticleNotFoundError
        if article.author_id != user.id:
            raise ForbiddenError

        try:
            tags = await self._repo.attach_tags(article.id, data)
        except IntegrityError:
            raise DuplicateOrMissingTagError

        return [ArticleTagDTO.model_validate(t) for t in tags]
