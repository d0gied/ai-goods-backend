import argparse

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from global_modules.enums import CeleryQueue
from vector_storage.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from vector_storage.tasks import get_tasks
from global_modules.db.repositories import GoodRepository

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

for task in get_tasks():
    app.register_task(
        task,
        queue="storage",
    )

logger = get_task_logger(__name__)

parser = argparse.ArgumentParser(description="Run vector storage worker")
parser.add_argument("--tasks", help="get list of tasks", action="store_true")
parser.add_argument("--worker", help="run worker", action="store_true")
parser.add_argument("--test", help="run test", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.tasks:
        for task in app.tasks:
            if task.startswith("celery."):
                continue
            print("--------------------------")
            print(f"Task: {task}")
            print(f"Queue: {CeleryQueue.STORAGE.value}")
    elif args.worker:
        app.worker_main()
    elif args.test:
        app.worker_main(
            argv=["worker", "-B", "-l", "INFO", "-E", "-Q", CeleryQueue.STORAGE]
        )
    else:
        app.start()
