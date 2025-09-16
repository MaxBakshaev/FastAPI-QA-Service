from fastapi import FastAPI
import uvicorn


application = FastAPI()


def run():
    uvicorn.run(
        "main:application",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run()
