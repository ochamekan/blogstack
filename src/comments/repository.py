from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.comments.models import Comment


class CommentsRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def create_or_update_comment(self, new_comment: Comment) -> Comment:
        self._db.add(new_comment)
        await self._db.commit()
        await self._db.refresh(new_comment)
        return new_comment

    async def delete_comment(self, comment_id: str, user_id: str) -> Comment:
        res = await self._db.execute(
            select(Comment).where(Comment.id == comment_id, Comment.user_id == user_id)
        )
        comment = res.scalar_one()
        await self._db.delete(comment)
        await self._db.commit()
        await self._db.refresh(comment)
        return comment

    async def get_comments_by_article_id(self, article_id: str) -> list[Comment]:
        res = await self._db.execute(
            select(Comment).where(Comment.article_id == article_id)
        )
        comments = list(res.scalars().all())
        return comments

    async def get_comment_by_id(self, comment_id: str) -> Comment | None:
        res = await self._db.execute(select(Comment).where(Comment.id == comment_id))
        return res.scalar_one_or_none()
