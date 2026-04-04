from typing import ClassVar
from pydantic import BaseModel, ConfigDict, Field


class CreateUserRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True,
        "extra": "ignore",
    }

    email: str = Field(min_length=6)
    password: str = Field(min_length=8)
    fullname: str = Field(min_length=5)


class CreateUserResponse(BaseModel):
    id: str
    email: str
    fullname: str
