import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Answer
from tests.test_mixin import QATestMixin as qa


@pytest.mark.asyncio
async def test_create_answer_for_question(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет добавление ответа к вопросу"""

    question = await qa.add_question(session)
    answer = await qa.add_answer(client, question.id)

    assert answer["text"] == "Гепард"
    assert answer["question_id"] == question.id

    answer_in_db = await session.get(Answer, answer["id"])
    assert answer_in_db is not None
    assert answer_in_db.text == "Гепард"


@pytest.mark.asyncio
async def test_create_answer_for_non_existing_question(
    client: AsyncClient,
):
    """Проверяет добавление ответа к несуществующему вопросу"""

    answer_data = {"text": "Ответ на несуществующий вопрос"}

    question_id = 7777777
    response = await client.post(
        f"/api/v1/questions/{question_id}/answers",
        json=answer_data,
    )
    assert response.status_code == 404
    assert f"Вопрос с id {question_id} не найден!" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_answer_by_id(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет получение ответа по id"""

    question = await qa.add_question(session)
    answer = await qa.add_answer(client, question.id, text="Гепард")

    get_response = await client.get(f"/api/v1/answers/{answer['id']}/")
    assert get_response.status_code == 200
    assert get_response.json() == answer


@pytest.mark.asyncio
async def test_get_answer_by_id_not_found(
    client: AsyncClient,
):
    """Проверяет получение несуществующего ответа по id"""

    answer_id = 66666
    response = await client.get(f"/api/v1/answers/{answer_id}/")
    assert response.status_code == 404
    assert f"Ответ с id {answer_id} не найден!" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_answer_by_id(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет удаление ответа по id"""

    question = await qa.add_question(session)
    answer = await qa.add_answer(
        client,
        question.id,
        text="Ответ для удаления",
    )

    response = await client.delete(f"/api/v1/answers/{answer['id']}/")
    assert response.status_code == 204

    deleted_answer = await session.get(Answer, answer["id"])
    assert deleted_answer is None


@pytest.mark.asyncio
async def test_delete_answer_not_found(
    client: AsyncClient,
):
    """Проверяет удаление несуществующего ответа"""

    answer_id = 55555
    response = await client.delete(f"/api/v1/answers/{answer_id}/")
    assert response.status_code == 404
    assert f"Ответ с id {answer_id} не найден!" in response.json()["detail"]
