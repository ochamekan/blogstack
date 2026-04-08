from src.auth.exceptions import (
    EmailAlreadyTakenError,
    InvalidCredentialsError,
    NotAuthenticatedError,
    UserNotFoundError,
)
from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemes import CreateUserRequest, LoginRequest
from src.security.exceptions import (
    InvalidTokenSignatureError,
    MalformedTokenError,
    TokenDecodeError,
    TokenExpiredError,
)
from src.security.jwt import (
    TokenType,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from src.security.schemes import RefreshTokenResponse, Tokens
from src.security.utils import hash_password, verify_password


class AuthService:
    def __init__(self, repo: AuthRepository):
        self._repo: AuthRepository = repo

    def signup(self, data: CreateUserRequest) -> User:
        if self._repo.get_user_by_email(data.email):
            raise EmailAlreadyTakenError

        user = User.model_validate(
            data, update={"hashed_password": hash_password(data.password)}
        )
        new_user = self._repo.create_user(user)
        return new_user

    def login(self, data: LoginRequest) -> Tokens:
        user = self._repo.get_user_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError

        access_token = create_access_token(
            email=user.email, user_id=user.id, role=user.role
        )
        refresh_token = create_refresh_token(user.id)
        return Tokens(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    def refresh(self, refresh_token: str) -> RefreshTokenResponse:
        try:
            claims = decode_token(refresh_token)
        except (
            TokenDecodeError,
            TokenExpiredError,
            InvalidTokenSignatureError,
            MalformedTokenError,
        ):
            raise InvalidTokenSignatureError

        id = claims.sub
        if not claims or not claims.type == TokenType.REFRESH or not id:
            raise InvalidTokenSignatureError

        user = self._repo.get_user_by_id(id)
        if not user:
            raise InvalidTokenSignatureError

        new_access_token = create_access_token(
            email=user.email, role=user.role, user_id=user.id
        )
        return RefreshTokenResponse(access_token=new_access_token, token_type="bearer")

    def get_user_by_id(self, id: str) -> User | None:
        user = self._repo.get_user_by_id(id)
        if not user:
            raise UserNotFoundError
        return user
