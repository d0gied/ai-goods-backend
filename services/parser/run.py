from argparse import ArgumentParser
from parser.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from parser.parsers.alibaba import AlibabaParser
from parser.parsers.ozon import OZONParser
from parser.parsers.wildberries import WildberriesParser
from parser.tasks.get_good import get_good_task_builder
from parser.tasks.get_goods import get_goods_task_builder

from celery import Celery

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

QUEUE = "parser"

sources = {
    "wildberries": WildberriesParser(),
    "alibaba": AlibabaParser(),
    "ozon": OZONParser(),
}

for source, parser in sources.items():
    app.register_task(get_goods_task_builder(source, parser), queue=QUEUE)
    print(f"Register task: {source}, queue: {QUEUE}")
    app.register_task(get_good_task_builder(source, parser), queue=QUEUE)
    print(f"Register task: {source}, queue: {QUEUE}")

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
