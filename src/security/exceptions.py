from src.exceptions import AppBaseException


class TokenDecodeError(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired token",
            error_code="INVALID_TOKEN",
            status_code=401,
        )


class TokenExpiredError(TokenDecodeError):
    def __init__(self):
        super().__init__()
        self.message: str = "Token has expired"
        self.error_code: str = "TOKEN_EXPIRED"


class InvalidTokenSignatureError(TokenDecodeError):
    def __init__(self):
        super().__init__()
        self.message: str = "Token signature is invalid."
        self.error_code: str = "INVALID_TOKEN_SIGNATURE"


class MalformedTokenError(TokenDecodeError):
    def __init__(self):
        super().__init__()
        self.message: str = "Malformed token claims."
        self.error_code: str = "MALFORMED_TOKEN"
