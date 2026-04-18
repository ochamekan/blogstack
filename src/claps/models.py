from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Clap(Base):
    __tablename__ = "claps"  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default_factory=lambda: str(uuid.uuid4()), init=False
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    article_id: Mapped[str] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"), nullable=False
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
        init=False,
    )
    __table_args__ = (  # pyright: ignore[reportAny, reportUnannotatedClassAttribute]
        UniqueConstraint("user_id", "article_id"),
        CheckConstraint("count <= 50", name="ck_claps_max_count_50"),
    )
