from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Request,
    Response,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, Answer, Question
from core.schemas import AnswerCreate, AnswerRead
from crud import answers_crud as crud
from utils import get_or_set_uuid

router = APIRouter(
    prefix=settings.api.v1.answers,
    tags=["Answers"],
)

qa_router = APIRouter(
    prefix=settings.api.v1.questions,
    tags=["Answers"],
)


@qa_router.post(
    "/{question_id}/answers",
    response_model=AnswerRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer_for_question(
    answer_in: AnswerCreate,
    request: Request,
    response: Response,
    question_id: int = Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создаёт и возвращает ответ на вопрос"""

    # UUID в cookie
    user_id = get_or_set_uuid(request, response)

    question = await session.get(
        Question,
        question_id,
    )
    if question is not None:
        answer = await crud.create_answer_for_question(
            session=session,
            answer_in=answer_in,
            question_id=question_id,
            user_id=user_id,
        )
        return answer

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Вопрос с id {question_id} не найден!",
    )


@router.get(
    "/{answer_id}/",
    response_model=AnswerRead,
)
async def get_answer_by_id(
    answer_id: int = Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Answer:
    """Возвращает ответ по id"""

    answer = await crud.get_answer_by_id(
        session=session,
        answer_id=answer_id,
    )
    if answer is not None:
        return answer

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ответ с id {answer_id} не найден!",
    )


@router.delete(
    "/{answer_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_answer_by_id(
    answer: Answer = Depends(get_answer_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """Удаляет ответ по id"""

    await crud.delete_answer_by_id(
        answer=answer,
        session=session,
    )
