from parser.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from parser.parsers.alibaba import AlibabaParser
from parser.parsers.ozon import OZONParser
from parser.parsers.wildberries import WildberriesParser
from parser.tasks.get_good import get_good_task_builder
from parser.tasks.get_goods import get_goods_task_builder

from argparse import ArgumentParser

from celery import Celery

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

sources = {
    "wildberries": WildberriesParser,
    "alibaba": AlibabaParser,
    "ozon": OZONParser,
}

for source, parser in sources.items():
    app.register_task(get_goods_task_builder(source, parser), queue=f"parse.{source}")
    app.register_task(get_good_task_builder(source, parser), queue=f"parse.{source}")

parser = ArgumentParser(description="Run vector storage worker")
parser.add_argument("--tasks", help="get list of tasks", action="store_true")
parser.add_argument("--worker", help="run worker", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.tasks:
        for task in app.tasks:
            print(task)
    elif args.worker:
        app.worker_main()
    else:
        app.start()