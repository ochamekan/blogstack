from src.tags.models import Tag
from src.tags.repository import TagsRepository
from src.tags.schemas import TagDTO
from src.utils import get_slug


class TagsService:
    def __init__(self, repo: TagsRepository) -> None:
        self._repo: TagsRepository = repo

    async def create_tag(self, name: str) -> TagDTO:
        new_tag = Tag(name=name, slug=get_slug(name))
        created_tag = await self._repo.create_tag(new_tag)
        return TagDTO.model_validate(created_tag)

    async def get_tags(self, q: str) -> list[TagDTO]:
        tags = await self._repo.get_tags(q)
        return [TagDTO.model_validate(t) for t in tags]

    async def get_tag_by_name(self, name: str) -> TagDTO | None:
        tag = await self._repo.get_tag(name)
        return TagDTO.model_validate(tag)
