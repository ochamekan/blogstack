from sqlalchemy.ext.asyncio import AsyncSession


class CommentsRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def create_comment(self):
        pass
