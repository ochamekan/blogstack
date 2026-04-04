from typing import ClassVar
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True,
        "extra": "ignore",
    }

    email: EmailStr = Field(min_length=6)
    password: str = Field(min_length=8)
    fullname: str = Field(min_length=5)
    about: str | None = Field(default=None, min_length=10)


class CreateUserResponse(BaseModel):
    id: str
    email: str
    fullname: str
