from fastapi import status

from src.exceptions import AppBaseException


class UserNotFoundError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="User not found",
            error_code="USER_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class InvalidCredentialsError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials",
            error_code="INVALID_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class EmailAlreadyTakenError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Email already taken",
            error_code="EMAIL_ALREADY_TAKEN",
            status_code=status.HTTP_409_CONFLICT,
        )


class NotAuthenticatedError(AppBaseException):
    def __init__(self) -> None:
        super().__init__(
            message="Not authenticated",
            error_code="NOT_AUTHENTICATED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
