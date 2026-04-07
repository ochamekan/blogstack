from typing import Annotated

from fastapi import Depends

from src.auth.exceptions import InvalidToken, NotAuthenticated
from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.service import AuthService
from src.deps import SessionDep
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.security.jwt import TokenType, decode_token

bearer_scheme = HTTPBearer()


def get_auth_repo(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    repo: AuthRepositoryDep,
) -> AuthService:
    return AuthService(repo)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repo)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]


def get_current_user(service: AuthServiceDep, creds: TokenDep) -> User:
    try:
        token = creds.credentials
        claims = decode_token(token)
        id = claims.sub
        if not claims.type == TokenType.ACCESS or not id:
            raise InvalidToken
        user = service.get_user_by_id(id)
        if not user:
            raise NotAuthenticated
        return user
    except Exception:
        raise


UserDep = Annotated[User, Depends(get_current_user)]
