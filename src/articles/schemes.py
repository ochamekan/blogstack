from typing import ClassVar
from pydantic import BaseModel, ConfigDict, Field

from src.articles.models import Article, ArticleStatus


class CreateArticleRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True,
        "extra": "ignore",
    }

    title: str = Field(min_length=20)
    body: str


class UpdateArticleRequest(BaseModel):
    title: str | None = None
    body: str | None = None
    status: ArticleStatus | None = None


class GetArticlesResponse(BaseModel):
    total_pages: int
    current_page: int
    limit: int
    data: list[Article] = []
