from src.auth.exceptions import (
    EmailAlreadyTakenError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from src.auth.models import User
from src.auth.repository import AuthRepository
from src.auth.schemas import CreateUserRequest, LoginRequest, UserDTO
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
from src.security.schemas import RefreshTokenResponse, Tokens
from src.security.utils import hash_password, verify_password


class AuthService:
    def __init__(self, repo: AuthRepository):
        self._repo: AuthRepository = repo

    async def signup(self, data: CreateUserRequest) -> UserDTO:
        if await self._repo.get_user_by_email(data.email):
            raise EmailAlreadyTakenError

        new_user = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hash_password(data.password),
        )

        created_user = await self._repo.create_user(new_user)
        return UserDTO.model_validate(created_user)

    async def login(self, data: LoginRequest) -> Tokens:
        user = await self._repo.get_user_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError

        access_token = create_access_token(
            email=user.email, user_id=user.id, role=user.role
        )
        refresh_token = create_refresh_token(user.id)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token: str) -> RefreshTokenResponse:
        claims = decode_token(refresh_token)

        if claims.type != TokenType.REFRESH:
            raise InvalidTokenSignatureError

        user = await self._repo.get_user_by_id(claims.sub)
        if not user:
            raise InvalidTokenSignatureError

        new_access_token = create_access_token(
            email=user.email, role=user.role, user_id=user.id
        )
        return RefreshTokenResponse(access_token=new_access_token, token_type="bearer")

    async def get_user_by_id(self, id: str) -> UserDTO:
        user = await self._repo.get_user_by_id(id)
        if not user:
            raise UserNotFoundError
        return UserDTO.model_validate(user)
