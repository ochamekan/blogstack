from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User


class AuthRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self._db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, id: str) -> User | None:
        result = await self._db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def create_user(self, new_user: User) -> User:
        self._db.add(new_user)
        await self._db.commit()
        await self._db.refresh(new_user)
        return new_user
