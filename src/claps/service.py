from sqlalchemy.exc import IntegrityError
from src.articles.exceptions import ArticleNotFoundError
from src.articles.repository import ArticlesRepository
from src.auth.schemas import UserDTO
from src.claps.repository import ClapRepository
from src.claps.schemas import ClapDTO
from src.claps.exceptions import ClapsMaxCountError
from src.utils import get_constraint_name_from_integrity_error


class ClapService:
    def __init__(self, repo: ClapRepository, article_repo: ArticlesRepository):
        self._repo: ClapRepository = repo
        self._article_repo: ArticlesRepository = article_repo

    async def increment_clap(self, article_id: str, user: UserDTO) -> ClapDTO:
        article = await self._article_repo.get_article_by_id(article_id)
        if not article:
            raise ArticleNotFoundError

        clap = await self._repo.get_clap(article_id, user.id)

        if not clap:
            new_clap = await self._repo.create_clap(article_id, user.id)
            return ClapDTO.model_validate(new_clap)

        try:
            updated_clap = await self._repo.increment_clap(clap.id)
        except IntegrityError as e:
            constraint_name = get_constraint_name_from_integrity_error(e)
            if constraint_name == "ck_claps_max_count_50":
                raise ClapsMaxCountError
            raise

        return ClapDTO.model_validate(updated_clap)
