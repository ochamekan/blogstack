from pydantic import ValidationError
from src.auth.exceptions import (
    EmailAlreadyTaken,
    IncorrectPassword,
    NotAuthenticated,
    UserDoesNotExist,
)
from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemes import CreateUserRequest, LoginRequest
from src.security.jwt import create_access_token, create_refresh_token
from src.security.schemes import Tokens
from src.security.utils import hash_password, verify_password


class AuthService:
    def __init__(self, repo: AuthRepository):
        self._repo: AuthRepository = repo

    def signup(self, data: CreateUserRequest) -> User:
        if self._repo.get_user_by_email(data.email):
            raise EmailAlreadyTaken

        try:
            user = User.model_validate(
                data, update={"hashed_password": hash_password(data.password)}
            )
        except ValidationError:
            raise

        new_user = self._repo.create_user(user)
        return new_user

    def login(self, data: LoginRequest) -> Tokens:
        user = self._repo.get_user_by_email(data.email)
        if not user:
            raise UserDoesNotExist
        if not verify_password(data.password, user.hashed_password):
            raise IncorrectPassword

        access_token = create_access_token(
            email=user.email, user_id=user.id, role=user.role
        )
        refresh_token = create_refresh_token(user.id)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    def get_user_by_id(self, id: str) -> User | None:
        user = self._repo.get_user_by_id(id)
        if not user:
            raise UserDoesNotExist
        if not id == user.id:
            raise NotAuthenticated
        return user
