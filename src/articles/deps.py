from typing import Annotated
from fastapi import Depends
from src.articles.repository import ArticlesRepository
from src.articles.service import ArticlesService
from src.deps import SessionDep


def get_articles_repo(db: SessionDep) -> ArticlesRepository:
    return ArticlesRepository(db)


ArticlesRepoDep = Annotated[ArticlesRepository, Depends(get_articles_repo)]


def get_articles_service(repo: ArticlesRepoDep) -> ArticlesService:
    return ArticlesService(repo)


ArticleServiceDep = Annotated[ArticlesService, Depends(get_articles_service)]
