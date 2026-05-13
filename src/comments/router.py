from fastapi import APIRouter

from src.auth.deps import UserDep
from src.comments.deps import CommentsServiceDep
from src.comments.schemas import CommentDTO, CreateCommentRequest


router = APIRouter(tags=["comments"], prefix="/comments")


@router.post("/{article_id}", response_model=CommentDTO)
async def create_comment(
    service: CommentsServiceDep,
    user: UserDep,
    article_id: str,
    data: CreateCommentRequest,
):
    return await service.create_comment(article_id, data, user)
