from fastapi import APIRouter, HTTPException, status

from src.auth.deps import AuthServiceDep, UserDep
from src.auth.exceptions import EmailAlreadyTaken, IncorrectPassword, UserDoesNotExist
from src.auth.schemes import (
    CreateUserRequest,
    CreateUserResponse,
    GetCurrentUserRequest,
    LoginRequest,
)
from src.security.schemes import Tokens


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(body: LoginRequest, service: AuthServiceDep) -> Tokens:
    try:
        return service.login(body)
    except UserDoesNotExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
    except IncorrectPassword as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
    except Exception:
        raise


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def signup(body: CreateUserRequest, service: AuthServiceDep):
    try:
        return service.signup(body)
    except EmailAlreadyTaken as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err.detail)
    except Exception:
        raise


@router.get("/me", response_model=GetCurrentUserRequest)
async def read_user(user: UserDep):
    return user
