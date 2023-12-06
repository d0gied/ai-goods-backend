from celery import current_app
from celery.result import AsyncResult

from ..enums import Source
from ..parsers.base import Parser
from .base import BaseTask


class GetGoodsTask(BaseTask):
    """Parser task with prerealized logic for parsing to be used in subclasses
    Scrapes goods from source

    Args:
        name (str): name of the task
        parser (Parser): parser instance
    """

    def __init__(self, name: str, parser: Parser):
        super().__init__(f"get_goods.{name}")
        self.parser = parser

    def run(self, request: str, *, limit=100, **kwargs) -> list[dict]:
        """Run the task"""

        # TODO: add logging
        # TODO: add error handling
        # TODO: add retrying
        # TODO: add saving storage(db, file system, S3, etc.)
        # TODO: change returning value to returning file name

        goods = self.parser.get_goods(request, limit=limit, **kwargs)
        goods = [good.model_dump() for good in goods]
        return goods


class GetGoodsMultipleSourcesTask(BaseTask):
    """Parser task with prerealized logic for parsing to be used in subclasses
    Scrapes goods from multiple sources
    """

    def __init__(self):
        super().__init__(f"get_goods")

    def run(
        self, request: str, sources: list[Source], *, limit_per_source=100, **kwargs
    ) -> dict[str, dict]:
        """Run the task"""

        # TODO: add logging
        # TODO: add error handling

        requests: dict[str, AsyncResult] = {}
        for source in sources:
            requests[source] = current_app.send_task(
                f"parser.tasks.get_goods.{source.value}",
                args=[request],
                kwargs={"limit": limit_per_source},
                queue=f"parse_{source.value}",
            )

        goods: dict[str, dict] = {}
        for source in sources:
            goods[source] = requests[source].get()

        return goods

def get_goods_task_builder(name: str, parser: Parser) -> GetGoodsTask:
    """Get GetGoodTask instance"""
    return GetGoodsTask(name=name, parser=parser)

def get_goods_multiple_sources_task_builder() -> GetGoodsMultipleSourcesTask:
    """Get GetGoodTask instance"""
    return GetGoodsMultipleSourcesTask()
