from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, Question
from core.schemas import QuestionCreate, QuestionRead
from crud import questions_crud as crud

router = APIRouter(
    prefix=settings.api.v1.questions,
    tags=["Questions"],
)


@router.get("/", response_model=List[QuestionRead])
async def get_questions_list(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Возвращает список всех вопросов"""
    return await crud.get_questions_list(session=session)


@router.post(
    "/",
    response_model=QuestionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_question(
    question_in: QuestionCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Возвращает созданный вопрос"""
    return await crud.create_new_question(
        session=session,
        question_in=question_in,
    )


@router.get(
    "/{question_id}/",
    response_model=QuestionRead,
)
async def get_question_with_answers_by_id(
    question_id: int = Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Question:
    """Возвращает вопрос по id и все ответы на него"""
    question = await crud.get_question_with_answers_by_id(
        session=session,
        question_id=question_id,
    )
    if question is not None:
        return question

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Вопрос с id {question_id} не найден!",
    )


@router.delete(
    "/{question_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    question: Question = Depends(get_question_with_answers_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """Удаление продукта по id"""
    await crud.delete_question_with_answers_by_id(
        session=session,
        question=question,
    )
