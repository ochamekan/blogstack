import datetime
from enum import Enum
import uuid
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
)
from pydantic import BaseModel, EmailStr
from src.auth.models import Role
from src.config import settings


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class ClaimsBase(BaseModel):
    exp: datetime.datetime
    jti: uuid.UUID
    type: TokenType


class ATClaims(ClaimsBase):
    email: EmailStr
    role: Role
    sub: str


class RTClaims(ClaimsBase):
    sub: str


def create_access_token(email: str, role: Role, user_id: str) -> str:
    claims = ATClaims(
        email=email,
        role=role,
        exp=datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        jti=uuid.uuid4(),
        type=TokenType.ACCESS,
        sub=user_id,
    )
    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload=claims.model_dump(mode="json"),
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: str) -> str:
    claims = RTClaims(
        sub=user_id,
        type=TokenType.REFRESH,
        exp=datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        jti=uuid.uuid4(),
    )
    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload=claims.model_dump(mode="json"),
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> ATClaims | RTClaims:
    try:
        data = jwt.decode(  # pyright: ignore[reportUnknownMemberType]
            token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    if data.get("type") == TokenType.ACCESS:
        return ATClaims.model_validate(data)
    elif data.get("type") == TokenType.REFRESH:
        return RTClaims.model_validate(data)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token claims"
        )
