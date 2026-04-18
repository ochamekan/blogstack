from pydantic import BaseModel, Field, ConfigDict
from typing import ClassVar


class AttachTagsRequest(BaseModel):
    data: list[str] = Field(min_length=1)


class ArticleTagDTO(BaseModel):
    model_config: ClassVar[ConfigDict] = {"from_attributes": True}

    article_id: str
    tag_id: str
