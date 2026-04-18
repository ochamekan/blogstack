import uuid
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Tag(Base):
    __tablename__ = "tags"  # pyright: ignore[reportUnannotatedClassAttribute]

    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default_factory=lambda: str(uuid.uuid4()), init=False
    )

    __table_args__ = (UniqueConstraint("name", "slug"),)  # pyright: ignore[reportUnannotatedClassAttribute]
