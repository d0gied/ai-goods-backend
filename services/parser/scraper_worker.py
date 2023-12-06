from parser.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from parser.tasks.get_goods import get_goods_multiple_sources_task_builder

from celery import Celery

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

app.register_task(get_goods_multiple_sources_task_builder(), queue="scrape")

if __name__ == "__main__":
    app.start()
