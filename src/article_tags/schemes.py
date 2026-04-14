from pydantic import BaseModel, Field


class AttachTagsRequest(BaseModel):
    data: list[str] = Field(min_length=1)
