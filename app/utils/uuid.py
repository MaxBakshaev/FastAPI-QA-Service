from fastapi import Request, Response
from typing import Optional
import uuid


def get_or_set_uuid(
    request: Request,
    response: Response,
) -> str:
    """
    Получает UUID из user_id в cookie, если не существует,
    то создает его и возвращает
    """
    user_id: Optional[str] = request.cookies.get("user_id")
    if user_id is None:
        user_id = str(uuid.uuid4())
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            max_age=60 * 60 * 24 * 30,
        )
    return user_id
