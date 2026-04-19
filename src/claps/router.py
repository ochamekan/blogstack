from fastapi import APIRouter

from src.auth.deps import UserDep
from src.claps.deps import ClapServiceDep
from src.claps.schemas import DeleteClapsResponse, IncrementClapsResponse


router = APIRouter(tags=["article claps"], prefix="/article")


@router.post("/{article_id}/claps", response_model=IncrementClapsResponse)
async def increment_clap(service: ClapServiceDep, user: UserDep, article_id: str):
    return await service.increment_clap(article_id=article_id, user=user)


@router.delete("/{article_id}/claps", response_model=DeleteClapsResponse)
async def delete_claps(service: ClapServiceDep, user: UserDep, article_id: str):
    return await service.delete_claps(article_id=article_id, user=user)
