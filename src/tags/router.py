from fastapi import APIRouter

from src.auth.deps import UserDep
from src.tags.deps import TagsServiceDep
from src.tags.schemas import CreateTagRequest, TagDTO


router = APIRouter(tags=["tags"], prefix="/tags")


@router.post("", response_model=TagDTO)
async def create_tag(service: TagsServiceDep, body: CreateTagRequest, _: UserDep):
    return await service.create_tag(body.name)


@router.get("", response_model=list[TagDTO])
async def get_tags(service: TagsServiceDep, q: str = ""):
    return await service.get_tags(q)
