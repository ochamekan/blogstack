from fastapi import APIRouter

from src.deps import SessionDep


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(session: SessionDep):
    pass


@router.post("/signup")
async def signup(session: SessionDep):
    pass
