from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question


class QuestionTestMixin:
    question_text = "Какое самое быстрое наземное животное?"

    @staticmethod
    async def delete_records_from_questions(session: AsyncSession):
        await session.execute(text("DELETE FROM questions"))
        await session.commit()

    @staticmethod
    async def add_question(
        session: AsyncSession,
        text: str = None,
    ) -> Question:
        text = text or QuestionTestMixin.question_text

        question = Question(text=text)
        session.add(question)

        await session.commit()
        await session.refresh(question)

        return question
