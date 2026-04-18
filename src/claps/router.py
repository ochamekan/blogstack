from fastapi import APIRouter

from src.auth.deps import UserDep
from src.claps.deps import ClapServiceDep
from src.claps.schemas import ClapDTO


router = APIRouter(tags=["article claps"], prefix="/article")


@router.post("/{article_id}/claps", response_model=ClapDTO)
async def increment_clap(service: ClapServiceDep, user: UserDep, article_id: str):
    return await service.increment_clap(article_id=article_id, user=user)
