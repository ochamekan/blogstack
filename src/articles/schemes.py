from typing import ClassVar
from pydantic import BaseModel, ConfigDict, Field


class CreateArticleRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True,
        "extra": "ignore",
    }

    title: str = Field(min_length=20)
    body: str
