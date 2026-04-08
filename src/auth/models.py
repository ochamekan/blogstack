from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
import uuid


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    __tablename__: str = "users"  # pyright: ignore[reportIncompatibleVariableOverride]

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    fullname: str = Field(nullable=False, min_length=5)
    about: str | None = Field(default=None)
    role: Role = Field(default=Role.USER.value, nullable=False)

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
        ),
    )
