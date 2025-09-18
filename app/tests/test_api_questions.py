from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question
from tests.test_mixin import QATestMixin as qa


@pytest.mark.asyncio
async def test_get_questions_empty(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет возвращение пустого списка из в БД без вопросов"""

    response = await client.get("/api/v1/questions/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_questions_with_data(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет возвращение корректных данных из БД с вопросом"""

    await qa.add_question(session, qa.question_text)

    response = await client.get("/api/v1/questions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["text"] == qa.question_text


@pytest.mark.asyncio
async def test_create_new_question(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет добавления вопроса в БД"""

    question_data = {"text": qa.question_text}

    response = await client.post(
        "/api/v1/questions/",
        json=question_data,
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["text"] == question_data["text"]

    question_in_db = await session.get(Question, data["id"])
    assert question_in_db is not None
    assert question_in_db.text == question_data["text"]


@pytest.mark.asyncio
async def test_get_question_with_answers_by_id(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет получение вопроса по id с его ответами"""

    question = await qa.add_question(session, qa.question_text)

    response = await client.get(f"/api/v1/questions/{question.id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question.id
    assert data["text"] == question.text

    assert "answers" in data
    assert isinstance(data["answers"], list)


@pytest.mark.asyncio
async def test_get_question_with_answers_by_id_not_found(
    client: AsyncClient,
):
    """Проверяет получение несуществующего вопроса по id"""

    question_id = 999999
    response = await client.get(f"/api/v1/questions/{question_id}/")
    assert response.status_code == 404
    data = response.json()
    assert f"Вопрос с id {question_id} не найден!" in data["detail"]


@pytest.mark.asyncio
async def test_delete_question_with_answers_by_id(
    client: AsyncClient,
    session: AsyncSession,
):
    """Проверяет удаления вопроса по id с его ответами"""

    question = await qa.add_question(session, qa.question_text)

    response = await client.delete(f"/api/v1/questions/{question.id}/")
    assert response.status_code == 204

    response = await client.get(f"/api/v1/questions/{question.id}/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_question_with_answers_by_id_not_found(
    client: AsyncClient,
):
    """Проверяет удаление несуществующего вопроса по id"""

    question_id = 888888
    response = await client.delete(f"/api/v1/questions/{question_id}/")
    assert response.status_code == 404
    data = response.json()
    assert f"Вопрос с id {question_id} не найден!" in data["detail"]
