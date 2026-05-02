from fastapi import APIRouter

from core.config import settings

router = APIRouter(tags=["meta"])


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": settings.APP_NAME}
