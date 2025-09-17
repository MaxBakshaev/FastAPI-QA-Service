from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import AnswerCreate
from core.models import Answer


async def create_answer_for_question(
    answer_in: AnswerCreate,
    question_id: int,
    session: AsyncSession,
    user_id: str,
) -> Answer:
    """Создает и возвращает ответ к вопросу по id вопроса"""

    answer = Answer(
        **answer_in.model_dump(),
        question_id=question_id,
        user_id=user_id,
    )
    session.add(answer)
    await session.commit()
    await session.refresh(answer)

    return answer


async def get_answer_by_id(
    answer_id: int,
    session: AsyncSession,
) -> Answer | None:
    """Возвращает ответ по id"""

    answer = await session.get(Answer, answer_id)
    return answer


async def delete_answer_by_id(
    answer: Answer,
    session: AsyncSession,
) -> None:
    """Удаляет ответ по id"""

    await session.delete(answer)
    await session.commit()
