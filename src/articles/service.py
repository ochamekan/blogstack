from src.articles.exceptions import (
    ArticleNotFoundError,
    ForbiddenError,
    TitleAlreadyExistsError,
)
from src.articles.models import Article, ArticleStatus
from src.articles.repository import ArticlesRepository
from src.articles.schemes import (
    CreateArticleRequest,
    GetArticlesResponse,
    UpdateArticleRequest,
)
from src.articles.utils import get_reading_time
from src.auth.models import User
from src.utils import get_slug


class ArticlesService:
    def __init__(self, repo: ArticlesRepository) -> None:
        self._repo: ArticlesRepository = repo

    async def get_articles(self, page: int, limit: int) -> GetArticlesResponse:
        articles, total_pages = await self._repo.get_articles(page, limit)
        return GetArticlesResponse(
            total_pages=total_pages, current_page=page, limit=limit, data=articles
        )

    async def create_article(self, data: CreateArticleRequest, user: User) -> Article:
        slug = get_slug(data.title)
        if await self._repo.get_article_by_slug(slug):
            raise TitleAlreadyExistsError

        a = Article(
            slug=slug,
            body=data.body,
            title=data.title,
            author_id=user.id,
            reading_time=get_reading_time(data.body),
            status=ArticleStatus.PUBLISHED,
        )
        new_article = await self._repo.create_article(a)
        return new_article

    async def get_aricle_by_slug(self, slug: str) -> Article:
        article = await self._repo.get_article_by_slug(slug)
        if not article:
            raise ArticleNotFoundError
        return article

    async def update_article(
        self, data: UpdateArticleRequest, slug: str, user: User
    ) -> Article:
        article = await self._repo.get_article_by_slug(slug)
        if not article:
            raise ArticleNotFoundError
        if not article.author_id == user.id:
            raise ForbiddenError

        if data.title and await self._repo.get_article_by_slug(get_slug(data.title)):
            raise TitleAlreadyExistsError

        if data.body:
            article.body = data.body
        if data.title:
            article.slug = get_slug(data.title)
            article.title = data.title
        if data.status:
            article.status = data.status

        return await self._repo.update_article(article)
