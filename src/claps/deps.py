from typing import Annotated

from fastapi import Depends

from src.articles.deps import ArticlesRepoDep
from src.claps.repository import ClapRepository
from src.claps.service import ClapService
from src.deps import SessionDep


def get_clap_repo(db: SessionDep) -> ClapRepository:
    return ClapRepository(db)


ClapRepoDep = Annotated[ClapRepository, Depends(get_clap_repo)]


def get_clap_service(repo: ClapRepoDep, article_repo: ArticlesRepoDep) -> ClapService:
    return ClapService(repo=repo, article_repo=article_repo)


ClapServiceDep = Annotated[ClapService, Depends(get_clap_service)]
