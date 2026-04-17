from pydantic import BaseModel, Field


class AttachTagsRequest(BaseModel):
    data: list[str] = Field(min_length=1)


class ArticleTagDTO(BaseModel):
    article_id: str
    tag_id: str
