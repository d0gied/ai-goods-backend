from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


def get_celery_app():
    celery_app = Celery(
        "api",
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
    )
    return celery_app
