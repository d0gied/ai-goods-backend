from argparse import ArgumentParser

from agent.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from agent.tasks import get_tasks
from celery import Celery

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

for task in get_tasks():
    app.register_task(task, queue=task.queue)

parser = ArgumentParser(description="Run vector storage worker")
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
            print(f"Queue: {app.tasks[task].queue}")

    elif args.worker:
        app.worker_main()
    elif args.test:
        app.worker_main(argv=["worker", "-l", "info", "-P", "solo"])
    else:
        app.start()
