from fastapi import status
from src.exceptions import AppBaseException


class DuplicateOrMissingTagError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Duplicate tag or missing tag",
            error_code="DUPLICATE_OR_MISSING_TAG",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
