import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.test_mixin import QATestMixin as qa


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_msg",
    [
        ({}, "Field required"),  # Нет поля text
        ({"text": ""}, "String should have at least 1 character"),
        ({"text": 123}, "Input should be a valid string"),
    ],
)
async def test_answer_create_validation(
    client: AsyncClient,
    session: AsyncSession,
    payload,
    expected_msg,
):
    """Проверяет валидацию при создании вопроса"""

    question = await qa.add_question(session)

    response = await client.post(
        f"/api/v1/questions/{question.id}/answers",
        json=payload,
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(expected_msg in err["msg"] for err in errors)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_msg",
    [
        ({}, "Field required"),
        ({"text": ""}, "String should have at least 1 character"),
        ({"text": 123}, "Input should be a valid string"),
    ],
)
async def test_question_create_validation(
    client: AsyncClient,
    payload,
    expected_msg,
):
    """Проверяет валидацию при создании ответа на вопрос"""

    response = await client.post("/api/v1/questions/", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(expected_msg in err["msg"] for err in errors)
