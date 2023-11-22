from parser.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from parser.parsers.alibaba import AlibabaParser
from parser.parsers.ozon import OZONParser
from parser.parsers.wildberries import WildberriesParser
from parser.tasks.get_good import get_good_from_source_task_builder
from parser.tasks.get_goods import get_goods_from_source_task_builder

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
    app.register_task(get_goods_from_source_task_builder(source, parser), queue="parse")
    app.register_task(get_good_from_source_task_builder(source, parser), queue="parse")

if __name__ == "__main__":
    app.start()
