from typing import Annotated

from fastapi import Depends
from src.article_tags.repository import ArticleTagsRepository
from src.article_tags.service import ArticleTagsService
from src.articles.deps import ArticlesRepoDep
from src.deps import SessionDep


def get_article_tags_repo(db: SessionDep) -> ArticleTagsRepository:
    return ArticleTagsRepository(db)


ArticleTagsRepoDep = Annotated[ArticleTagsRepository, Depends(get_article_tags_repo)]


def get_article_tags_service(
    articles_repo: ArticlesRepoDep,
    repo: ArticleTagsRepoDep,
) -> ArticleTagsService:
    return ArticleTagsService(articles_repo=articles_repo, repo=repo)


ArticleTagsServiceDep = Annotated[ArticleTagsService, Depends(get_article_tags_service)]
