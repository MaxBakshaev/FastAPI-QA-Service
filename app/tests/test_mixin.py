from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question


class QATestMixin:
    question_text = "Какое самое быстрое наземное животное?"

    @staticmethod
    async def add_question(
        session: AsyncSession,
        text: str = None,
    ) -> Question:
        text = text or QATestMixin.question_text

        question = Question(text=text)
        session.add(question)

        await session.commit()
        await session.refresh(question)

        return question

    @staticmethod
    async def add_answer(
        client: AsyncClient,
        question_id: int,
        text: str = "Гепард",
    ) -> dict:
        """Создаёт ответ через API и возвращает JSON-ответ"""

        response = await client.post(
            f"/api/v1/questions/{question_id}/answers",
            json={"text": text},
        )
        response.raise_for_status()

        return response.json()
