from datetime import datetime
from typing import ClassVar
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from src.auth.models import Role


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
    about: str | None = None
    role: Role


class LoginRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True,
        "extra": "ignore",
    }

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserDTO(BaseModel):
    id: str
    email: str
    fullname: str
    about: str | None = None
    role: Role
    created_at: datetime
    updated_at: datetime
