from fastapi import APIRouter, HTTPException, status

from src.auth.deps import AuthServiceDep
from src.auth.exceptions import EmailAlreadyTaken
from src.auth.schemes import CreateUserRequest, CreateUserResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(_: AuthServiceDep):
    pass


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def signup(body: CreateUserRequest, service: AuthServiceDep):
    try:
        return service.signup(body)
    except EmailAlreadyTaken as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
    except Exception:
        raise
        # raise HTTPException(
        #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     detail="Internal server error occured.",
        # )
