from fastapi import APIRouter, status

from src.auth.deps import AuthServiceDep
from src.auth.schemes import CreateUserRequest, CreateUserResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(_: AuthServiceDep):
    pass


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def signup(body: CreateUserRequest, service: AuthServiceDep):
    return service.signup(body)
