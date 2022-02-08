from fastapi import APIRouter

from app import schemas
from app.services import inspect_pool

router = APIRouter(tags=["health"])


@router.get("/health", response_model=schemas.Health)
async def read_root():
    return {
        "online": len([bot for bot in inspect_pool if bot.is_ready()]),
        "total": len(inspect_pool),
        "concurrency": inspect_pool.queue.qsize(),
    }
