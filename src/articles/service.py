from src.articles.exceptions import (
    ArticleNotFoundError,
    ForbiddenError,
    ArticleDuplicateTitleError,
)
from src.articles.models import Article, ArticleStatus
from src.articles.repository import ArticlesRepository
from src.articles.schemas import (
    ArticleDTO,
    CreateArticleRequest,
    GetArticlesResponse,
    UpdateArticleRequest,
)
from src.articles.utils import get_reading_time
from src.auth.schemas import UserDTO
from src.utils import get_slug


class ArticlesService:
    def __init__(self, repo: ArticlesRepository) -> None:
        self._repo: ArticlesRepository = repo

    async def get_articles(self, page: int, limit: int) -> GetArticlesResponse:
        articles, total_pages = await self._repo.get_articles(page, limit)
        return GetArticlesResponse(
            total_pages=total_pages,
            current_page=page,
            limit=limit,
            data=[ArticleDTO.model_validate(a) for a in articles],
        )

    async def create_article(
        self, data: CreateArticleRequest, user: UserDTO
    ) -> ArticleDTO:
        slug = get_slug(data.title)
        if await self._repo.get_article_by_slug(slug):
            raise ArticleDuplicateTitleError

        new_article = Article(
            slug=slug,
            body=data.body,
            title=data.title,
            author_id=user.id,
            reading_time=get_reading_time(data.body),
            status=ArticleStatus.PUBLISHED,
        )
        a = await self._repo.create_article(new_article)
        return ArticleDTO.model_validate(a)

    async def get_article_by_slug(self, slug: str) -> ArticleDTO:
        article = await self._repo.get_article_by_slug(slug)
        if not article:
            raise ArticleNotFoundError
        return ArticleDTO.model_validate(article)

    async def get_article_by_id(self, id: str) -> ArticleDTO:
        article = await self._repo.get_article_by_id(id)
        if not article:
            raise ArticleNotFoundError
        return ArticleDTO.model_validate(article)

    async def update_article(
        self, data: UpdateArticleRequest, id: str, user: UserDTO
    ) -> ArticleDTO:
        article = await self._repo.get_article_by_id(id)
        if not article:
            raise ArticleNotFoundError
        if not article.author_id == user.id:
            raise ForbiddenError

        if data.title and article.title == data.title:
            raise ArticleDuplicateTitleError

        if data.body:
            article.body = data.body
        if data.title:
            article.slug = get_slug(data.title)
            article.title = data.title
        if data.status:
            article.status = data.status

        updated_article = await self._repo.update_article(article)

        return ArticleDTO.model_validate(updated_article)
