from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from routers import api_router, test_router
from core.config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/#lifespan-function
    Закрывает сессию после завершения работы приложения
    """
    yield
    await db_helper.dispose()


application = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

application.include_router(api_router)
application.include_router(test_router)


def run():
    uvicorn.run(
        "main:application",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )


if __name__ == "__main__":
    run()
