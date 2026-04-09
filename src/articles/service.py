from src.articles.models import Article, ArticleStatus
from src.articles.repository import ArticlesRepository
from src.articles.schemes import CreateArticleRequest
from src.articles.utils import get_reading_time
from src.auth.models import User


class ArticlesService:
    def __init__(self, repo: ArticlesRepository) -> None:
        self._repo: ArticlesRepository = repo

    async def create_article(self, data: CreateArticleRequest, user: User) -> Article:
        reading_time = get_reading_time(data.body)
        new_slug = "-".join(data.title.lower().split(" "))
        a = Article(
            slug=new_slug,
            body=data.body,
            title=data.title,
            author_id=user.id,
            reading_time=reading_time,
            status=ArticleStatus.PUBLISHED,
        )
        new_article = await self._repo.create_article(a)
        return new_article
