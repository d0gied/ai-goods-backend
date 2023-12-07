from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from ml.tasks import get_image_tasks, get_name_tasks
from global_modules.enums import CeleryQueue
import argparse
from ml.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

for task in get_image_tasks():
    app.register_task(
        task,
        queue=CeleryQueue.ML_IMAGE,
    )

for task in get_name_tasks():
    app.register_task(
        task,
        queue=CeleryQueue.ML_NAME,
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
            print(task)
    elif args.worker:
        app.worker_main()
    elif args.test:
        app.worker_main(argv=["worker", "-B", "-l", "INFO", "-E", "-Q", CeleryQueue.STORAGE])
    else:
        app.start()