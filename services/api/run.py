import fastapi
from api.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, HOST, PORT
from api.routers import get_routers
from celery import Celery
from fastapi.responses import JSONResponse

app = fastapi.FastAPI()

for router in get_routers():
    app.include_router(router)


@app.get("/")
def read_root():
    return JSONResponse({"Hello": "World"})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
