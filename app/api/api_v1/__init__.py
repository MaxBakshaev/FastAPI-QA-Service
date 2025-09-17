from fastapi import APIRouter

from core.config import settings
from .questions import router as questions_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(questions_router)
