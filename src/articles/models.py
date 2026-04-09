from datetime import datetime, timezone
from enum import Enum
import uuid
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import Enum as SAEnum


class ArticleStatus(Enum):
    PUBLISHED = "published"
    ARCHIVED = "archived"
    UNLISTED = "unlisted"
    DRAFT = "draft"


class Article(Base):
    __tablename__ = "articles"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), init=False
    )
    reading_time: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(70), nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[ArticleStatus] = mapped_column(
        SAEnum(
            ArticleStatus,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],  # pyright: ignore[reportUnknownLambdaType, reportUnknownMemberType, reportUnknownVariableType]
        ),
        nullable=False,
        default=ArticleStatus.PUBLISHED,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        init=False,
    )
