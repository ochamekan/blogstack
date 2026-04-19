from typing import ClassVar
from pydantic import BaseModel, ConfigDict


class CommentDTO(BaseModel):
    model_config: ClassVar[ConfigDict] = {"from_attributes": True}

    id: str
    user_id: str
    article_id: str
    parent_id: str
    content: str
    is_deleted: bool
    created_at: str
    updated_at: str


class CreateCommentRequest(BaseModel):
    parent_id: str | None
    content: str
