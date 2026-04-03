import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    name: str = Field(nullable=False, min_length=2)
    surname: str = Field(nullable=False, min_length=2)
    about: str | None = Field(default=None)
