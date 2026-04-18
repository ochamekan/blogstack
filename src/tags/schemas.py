from pydantic import BaseModel, Field, ConfigDict
from typing import ClassVar


class CreateTagRequest(BaseModel):
    name: str = Field(min_length=1, max_length=32)


class TagDTO(BaseModel):
    model_config: ClassVar[ConfigDict] = {"from_attributes": True}

    name: str
    slug: str
    id: str
