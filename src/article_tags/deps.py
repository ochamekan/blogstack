from typing import Annotated

from fastapi import Depends
from src.article_tags.repository import ArticleTagsRepository
from src.article_tags.service import ArticleTagsService
from src.articles.deps import ArticleServiceDep
from src.deps import SessionDep


def get_article_tags_repo(db: SessionDep) -> ArticleTagsRepository:
    return ArticleTagsRepository(db)


def get_article_tags_service(
    articles_service: ArticleServiceDep, repo: ArticleTagsRepoDep, db: SessionDep
) -> ArticleTagsService:
    return ArticleTagsService(articles_service=articles_service, repo=repo, db=db)


ArticleTagsRepoDep = Annotated[ArticleTagsRepository, Depends(get_article_tags_repo)]
ArticleTagsServiceDep = Annotated[ArticleTagsService, Depends(get_article_tags_service)]
