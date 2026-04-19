from src.articles.exceptions import ArticleNotFoundError
from src.articles.repository import ArticlesRepository
from src.auth.schemas import UserDTO
from src.comments.models import Comment
from src.comments.repository import CommentsRepository
from src.comments.schemas import CommentDTO, CreateCommentRequest


class CommentsService:
    def __init__(
        self, repo: CommentsRepository, article_repo: ArticlesRepository
    ) -> None:
        self._repo: CommentsRepository = repo
        self._article_repo: ArticlesRepository = article_repo

    async def create_comment(
        self, article_id: str, data: CreateCommentRequest, user: UserDTO
    ) -> CommentDTO:
        article = await self._article_repo.get_article_by_id(article_id)
        if not article:
            raise ArticleNotFoundError

        c = Comment(
            user_id=user.id,
            is_deleted=False,
            content=data.content,
            article_id=article_id,
            parent_id=data.parent_id,
        )
        new_comment = await self._repo.create_or_update_comment(c)
        return CommentDTO.model_validate(new_comment)
