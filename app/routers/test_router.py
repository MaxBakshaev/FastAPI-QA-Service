from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils import get_or_set_uuid

router = APIRouter()


@router.get("/test")
def get_user_id(request: Request, response: JSONResponse):
    user_id = get_or_set_uuid(request, response)
    return {"user_id": user_id}
