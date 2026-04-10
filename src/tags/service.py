from src.tags.models import Tag
from src.tags.repository import TagsRepository
from src.utils import get_slug


class TagsService:
    def __init__(self, repo: TagsRepository) -> None:
        self._repo: TagsRepository = repo

    async def create_tag(self, name: str) -> Tag:
        new_tag = Tag(name=name, slug=get_slug(name))
        return await self._repo.create_tag(new_tag)

    async def get_tags(self, q: str) -> list[Tag]:
        return await self._repo.get_tags(q)
