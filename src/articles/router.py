from typing import Annotated
from fastapi import APIRouter, Query

from src.articles.deps import ArticleServiceDep
from src.articles.schemas import (
    ArticleDTO,
    CreateArticleRequest,
    GetArticlesResponse,
    UpdateArticleRequest,
)
from src.auth.deps import UserDep


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=GetArticlesResponse)
async def get_all_articles(
    service: ArticleServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1)] = 10,
):
    return await service.get_articles(page, limit)


@router.post("", response_model=ArticleDTO)
async def create_article(
    body: CreateArticleRequest, service: ArticleServiceDep, user: UserDep
):
    return await service.create_article(body, user)


@router.get("/{slug}", response_model=ArticleDTO)
async def get_article(service: ArticleServiceDep, slug: str):
    return await service.get_article_by_slug(slug)


@router.patch("/{id}", response_model=ArticleDTO)
async def update_article(
    body: UpdateArticleRequest, service: ArticleServiceDep, id: str, user: UserDep
):
    return await service.update_article(body, id, user)
