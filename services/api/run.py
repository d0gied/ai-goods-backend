import fastapi
from api.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, HOST, PORT
from api.routers import parse, search
from celery import Celery

app = fastapi.FastAPI()

app.include_router(search.router)
app.include_router(parse.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    celery = Celery(
        "tasks",
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
    )
    from celery.result import AsyncResult

    celery.send_task(
        "agent.tasks.parse.wildberries",
        args=["iphone 12"],
        kwargs={"limit": 10},
        queue="agent",
    )
    # import uvicorn

    # uvicorn.run(app, host=HOST, port=PORT)
