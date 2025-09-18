from fastapi.testclient import TestClient

from main import application
from utils import camel_case_to_snake_case


def test_camel_case_to_snake_case():
    """Преобразует строку из CamelCase в snake_case"""

    result = camel_case_to_snake_case("SnakeCase")
    assert result == "snake_case"


client = TestClient(application)


def delete_user_id_from_cookie():
    if "user_id" in client.cookies:
        del client.cookies["user_id"]


def test_generate_uuid_when_cookie_missing():
    """
    Создает и передает uuid в user_id, когда 'user_id' отсутствует
    в cookie, потом проверяет наличие user_id в cookie
    """

    delete_user_id_from_cookie()

    response = client.get("/test")
    assert response.status_code == 200
    assert "user_id" in response.cookies

    delete_user_id_from_cookie()


def test_return_existing_uuid():
    """Проверяет наличие существующего 'user_id' в cookie"""

    delete_user_id_from_cookie()

    # Первый запрос, чтобы получить user_id
    initial_response = client.get("/test")
    existing_user_id = initial_response.cookies.get("user_id")
    assert existing_user_id is not None

    delete_user_id_from_cookie()
    client.cookies.set("user_id", existing_user_id)

    # Второй запрос с существующим user_id
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json()["user_id"] == existing_user_id

    delete_user_id_from_cookie()
