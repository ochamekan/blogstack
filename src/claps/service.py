from src.articles.exceptions import ArticleNotFoundError
from src.articles.repository import ArticlesRepository
from src.auth.schemas import UserDTO
from src.claps.repository import ClapRepository
from src.claps.schemas import DeleteClapsResponse, IncrementClapsResponse


class ClapService:
    def __init__(self, repo: ClapRepository, article_repo: ArticlesRepository):
        self._repo: ClapRepository = repo
        self._article_repo: ArticlesRepository = article_repo

    async def increment_clap(
        self, article_id: str, user: UserDTO
    ) -> IncrementClapsResponse:
        article = await self._article_repo.get_article_by_id(article_id)
        if not article:
            raise ArticleNotFoundError

        clap = await self._repo.get_clap(article.id, user.id)
        if not clap:
            total = await self._repo.create_clap(article.id, user.id)
            return IncrementClapsResponse(total=total)

        total = await self._repo.increment_clap(clap.id, article.id)
        return IncrementClapsResponse(total=total)

    async def delete_claps(self, article_id: str, user: UserDTO) -> DeleteClapsResponse:
        total = await self._repo.delete_claps(article_id, user.id)
        return DeleteClapsResponse(total=total)
