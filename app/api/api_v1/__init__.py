from fastapi import APIRouter

from core.config import settings

from .answers import router as answers_router
from .answers import qa_router
from .questions import router as questions_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(answers_router)
router.include_router(qa_router)
router.include_router(questions_router)
