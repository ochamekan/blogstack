from typing import Annotated
from fastapi import APIRouter, Cookie, HTTPException, Response, status

from src.auth.deps import AuthServiceDep, UserDep
from src.auth.schemes import (
    CreateUserRequest,
    CreateUserResponse,
    GetCurrentUserRequest,
    LoginRequest,
    LoginResponse,
)
from src.security.schemes import RefreshTokenResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def signup(body: CreateUserRequest, service: AuthServiceDep):
    return service.signup(body)


@router.post("/login")
async def login(
    body: LoginRequest, service: AuthServiceDep, response: Response
) -> LoginResponse:
    tokens = service.login(body)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return LoginResponse(access_token=tokens.access_token, token_type="bearer")


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh(
    service: AuthServiceDep, refresh_token: Annotated[str | None, Cookie()]
):
    if not refresh_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No refresh token")
    return service.refresh(refresh_token)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="refresh_token", httponly=True, samesite="lax", secure=True
    )
    return {"message": "Logged out"}


@router.get("/me", response_model=GetCurrentUserRequest)
async def read_user(user: UserDep):
    return user
