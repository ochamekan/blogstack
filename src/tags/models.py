import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Tag(Base):
    __tablename__ = "tags"  # pyright: ignore[reportUnannotatedClassAttribute]

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default_factory=lambda: str(uuid.uuid4()), init=False
    )
