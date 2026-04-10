from fastapi import status
from src.exceptions import AppBaseException


class TitleAlreadyExistsError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Article with this title aready exists",
            error_code="USER_DUPLICATE_TITLE_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class ArticleNotFoundError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Article not found",
            error_code="ARTICLE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ForbiddenError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Forbidden",
            error_code="FORBIDDEN",
            status_code=status.HTTP_403_FORBIDDEN,
        )
