from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import ClassVar


class ClapDTO(BaseModel):
    model_config: ClassVar[ConfigDict] = {"from_attributes": True}

    id: str
    user_id: str
    article_id: str
    count: int = Field(le=50)
    created_at: datetime


class IncrementClapsResponse(BaseModel):
    total: int


class DeleteClapsResponse(BaseModel):
    total: int
