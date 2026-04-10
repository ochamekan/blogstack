from typing import Annotated
from fastapi import APIRouter, Query

from src.articles.deps import ArticleServiceDep
from src.articles.schemes import (
    CreateArticleRequest,
    GetArticlesResponse,
    UpdateArticleRequest,
)
from src.auth.deps import UserDep


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=GetArticlesResponse)
async def get_all(
    service: ArticleServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1)] = 10,
):
    return await service.get_articles(page, limit)


@router.post("")
async def create_article(
    body: CreateArticleRequest, service: ArticleServiceDep, user: UserDep
):
    return await service.create_article(body, user)


@router.get("/{slug}")
async def get_post(service: ArticleServiceDep, slug: str):
    return await service.get_aricle_by_slug(slug)


@router.put("/{slug}")
async def update_post(
    body: UpdateArticleRequest, service: ArticleServiceDep, slug: str, user: UserDep
):
    return await service.update_article(body, slug, user)
