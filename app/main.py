from fastapi import FastAPI
import uvicorn

from api import router as api_router


app = FastAPI()
app.include_router(
    api_router,
    prefix="/api",
)

application = FastAPI()
application.include_router(api_router)


def run():
    uvicorn.run(
        "main:application",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run()
