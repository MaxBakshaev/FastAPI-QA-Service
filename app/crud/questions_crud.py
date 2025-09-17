from typing import List
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.schemas import QuestionCreate
from core.models import Question


async def get_questions_list(session: AsyncSession) -> List[Question]:
    """Возвращает список всех вопросов"""
    stmt = (
        select(Question).
        options(selectinload(Question.answers)).
        order_by(Question.id)
    )
    result: Result = await session.execute(stmt)
    questions = result.scalars().all()
    return list(questions)


async def create_new_question(
    session: AsyncSession,
    question_in: QuestionCreate,
) -> Question:
    """Создает и возвращает вопрос с ответами"""
    question = Question(**question_in.model_dump())
    session.add(question)
    await session.commit()
    await session.refresh(question)
    stmt = (
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.id == question.id)
    )
    result = await session.execute(stmt)
    return result.scalar_one()


async def get_question_with_answers_by_id(
    session: AsyncSession,
    question_id: int,
) -> Question | None:
    """Возвращает вопрос по id и все ответы на него"""
    stmt = (
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.id == question_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_question_with_answers_by_id(
    session: AsyncSession,
    question: Question,
) -> None:
    """Удаляет вопрос и все ответы на него"""
    await session.delete(question)
    await session.commit()
