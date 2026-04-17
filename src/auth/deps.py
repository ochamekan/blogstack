from typing import Annotated

from fastapi import Depends
import jwt

from src.auth.exceptions import NotAuthenticatedError, UserNotFoundError
from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemas import UserDTO
from src.auth.service import AuthService
from src.deps import SessionDep
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.security.exceptions import (
    InvalidTokenSignatureError,
    MalformedTokenError,
    TokenDecodeError,
    TokenExpiredError,
)
from src.security.jwt import TokenType, decode_token

bearer_scheme = HTTPBearer()


def get_auth_repo(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repo)]


def get_auth_service(
    repo: AuthRepositoryDep,
) -> AuthService:
    return AuthService(repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]


async def get_current_user(service: AuthServiceDep, creds: TokenDep) -> UserDTO:
    token = creds.credentials

    try:
        claims = decode_token(token)
    except (
        TokenDecodeError,
        TokenExpiredError,
        InvalidTokenSignatureError,
        MalformedTokenError,
        jwt.PyJWTError,
    ):
        raise InvalidTokenSignatureError

    id = claims.sub
    if not claims or not claims.type == TokenType.ACCESS or not id:
        raise NotAuthenticatedError
    user = await service.get_user_by_id(id)
    if not user:
        raise UserNotFoundError
    return user


UserDep = Annotated[User, Depends(get_current_user)]
