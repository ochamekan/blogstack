from pydantic import BaseModel, Field


class CreateTagRequest(BaseModel):
    name: str = Field(min_length=1, max_length=32)


class TagDTO(BaseModel):
    name: str
    slug: str
    id: str
