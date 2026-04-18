from fastapi import status
from src.exceptions import AppBaseException


class ClapsMaxCountError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="User can't clap more than 50 times",
            error_code="CLAPS_MAX_COUNT_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
