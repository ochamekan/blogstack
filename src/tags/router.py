from fastapi import APIRouter

from src.auth.deps import UserDep
from src.tags.deps import TagsServiceDep
from src.tags.models import Tag
from src.tags.schemes import CreateTagRequest


router = APIRouter(tags=["tags"], prefix="/tags")


@router.post("")
async def create_tag(
    service: TagsServiceDep, body: CreateTagRequest, _: UserDep
) -> Tag:
    return await service.create_tag(body.name)


@router.get("")
async def get_tags(service: TagsServiceDep, q: str = "") -> list[Tag]:
    return await service.get_tags(q)
