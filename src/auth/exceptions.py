from fastapi import status


class EmailAlreadyTaken(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Email already taken"


class UserDoesNotExist(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "User with this email does not exist"


class IncorrectPassword(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Incorrect password"


class NotAuthenticated(Exception):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Not authenticated"


class InvalidToken(Exception):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Invalid token"
    headers: dict[str, str] = {"WWW-Authenticate": "Bearer"}


class InvalidCredentials(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Invalid credentials"
    headers: dict[str, str] = {"WWW-Authenticate": "Bearer"}
