from fastapi import APIRouter

from src.articles.deps import ArticleServiceDep
from src.articles.schemes import CreateArticleRequest
from src.auth.deps import UserDep


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("")
async def get_posts():
    pass


@router.post("")
async def create_article(
    body: CreateArticleRequest, service: ArticleServiceDep, user: UserDep
):
    return await service.create_article(body, user)


@router.get("/{slug}")
async def get_post(slug: str, user: UserDep):
    pass


@router.put("/{id}")
async def update_post(id: str, user: UserDep):
    pass
