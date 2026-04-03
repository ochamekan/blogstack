from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login():
    pass


@router.post("/signup")
async def signup():
    pass
