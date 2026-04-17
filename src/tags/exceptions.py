from fastapi import status
from src.exceptions import AppBaseException


class TagAlreadyExists(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Tag already exist",
            error_code="TAG_ALREADY_EXIST",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
