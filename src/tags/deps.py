from typing import Annotated
from fastapi import Depends

from src.deps import SessionDep
from src.tags.repository import TagsRepository
from src.tags.service import TagsService


def get_tags_repo(db: SessionDep) -> TagsRepository:
    return TagsRepository(db)


TagsRepoDep = Annotated[TagsRepository, Depends(get_tags_repo)]


def get_tags_service(repo: TagsRepoDep) -> TagsService:
    return TagsService(repo)


TagsServiceDep = Annotated[TagsService, Depends(get_tags_service)]
