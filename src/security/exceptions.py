from fastapi import status
from src.exceptions import AppBaseException


class TokenDecodeError(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired token",
            error_code="INVALID_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class TokenExpiredError(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Token has expired",
            error_code="TOKEN_EXPIRED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class InvalidTokenSignatureError(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Token signature is invalid.",
            error_code="INVALID_TOKEN_SIGNATURE",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class MalformedTokenError(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Malformed token claims.",
            error_code="MALFORMED_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
