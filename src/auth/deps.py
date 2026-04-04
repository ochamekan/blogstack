from typing import Annotated

from fastapi import Depends

from src.auth.repository import AuthRepository
from src.auth.service import AuthService
from src.deps import SessionDep


def get_auth_repo(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    repo: AuthRepositoryDep,
) -> AuthService:
    return AuthService(repo)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repo)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
