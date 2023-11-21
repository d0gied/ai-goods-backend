from parser.tasks.get_goods import GetGoodsTask

from celery import Celery

from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

app.register_task(GetGoodsTask(), queue="scrape")

if __name__ == "__main__":
    app.start()
