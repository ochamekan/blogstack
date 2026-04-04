from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.auth.repository import AuthRepository
from src.auth.service import AuthService


def get_auth_repo(db: Session) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    repo: AuthRepositoryDep,
) -> AuthService:
    return AuthService(repo)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repo)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
