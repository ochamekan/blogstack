from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel, ConfigDict, Field

from src.articles.models import ArticleStatus


class CreateArticleRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True,
        "extra": "ignore",
    }

    title: str = Field(min_length=20)
    body: str


class UpdateArticleRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True,
        "extra": "ignore",
    }

    title: str | None = Field(default=None, min_length=20)
    body: str | None = None
    status: ArticleStatus | None = None


class ArticleDTO(BaseModel):
    model_config: ClassVar[ConfigDict] = {"from_attributes": True}

    id: str
    reading_time: int
    author_id: str
    title: str
    body: str
    slug: str
    status: str
    created_at: datetime
    updated_at: datetime


class GetArticlesResponse(BaseModel):
    total_pages: int
    current_page: int
    limit: int
    data: list[ArticleDTO] = []
