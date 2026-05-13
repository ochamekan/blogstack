from typing import Annotated

from fastapi import Depends
from src.articles.deps import ArticlesRepoDep
from src.comments.repository import CommentsRepository
from src.comments.service import CommentsService
from src.deps import SessionDep


def get_comments_repo(db: SessionDep) -> CommentsRepository:
    return CommentsRepository(db)


CommentsRepoDep = Annotated[CommentsRepository, Depends(get_comments_repo)]


def get_comments_service(
    repo: CommentsRepoDep, article_repo: ArticlesRepoDep
) -> CommentsService:
    return CommentsService(repo, article_repo)


CommentsServiceDep = Annotated[CommentsService, Depends(get_comments_service)]
