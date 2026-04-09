from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import String, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from src.database import Base


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"  # pyright: ignore[reportUnannotatedClassAttribute]

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(
        SAEnum(Role, native_enum=False, values_callable=lambda x: [e.value for e in x]),  # pyright: ignore[reportUnknownLambdaType, reportUnknownMemberType, reportUnknownVariableType]
        nullable=False,
        default=Role.USER,
    )

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    about: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
