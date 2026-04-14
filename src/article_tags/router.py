from fastapi import APIRouter

from src.article_tags.deps import ArticleTagsServiceDep
from src.article_tags.schemes import AttachTagsRequest
from src.auth.deps import UserDep


router = APIRouter(prefix="/articles", tags=["article tags"])


@router.post("/{article_id}/tags")
async def attach_tags_to_article(
    service: ArticleTagsServiceDep,
    article_id: str,
    body: AttachTagsRequest,
    user: UserDep,
):
    return await service.attach_tags_to_article(article_id, body.data, user)
