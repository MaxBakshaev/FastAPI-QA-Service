from fastapi import FastAPI
import uvicorn

from api import router as api_router
from core.config import settings


app = FastAPI()

application = FastAPI()
application.include_router(api_router)


def run():
    uvicorn.run(
        "main:application",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )


if __name__ == "__main__":
    run()
