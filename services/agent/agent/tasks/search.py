import time
from typing import Literal

from celery import current_app
from celery.result import AsyncResult
from global_modules.db.repositories import GoodRepository
from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodDumped, GoodEmbedding, GoodEmbeddingDumped

from .base import BaseTask


def get_task(task: AsyncResult):
    while not task.ready():
        time.sleep(0.1)
    return task.get()


class LoadGoodsFromDBByIdsTask(BaseTask):
    def __init__(self):
        super().__init__("load_goods_from_db_by_ids")

    def run(self, ids: list[int]) -> list[GoodDumped]:
        goods = GoodRepository().get_by_ids(ids)
        return [Good.from_orm(good) for good in goods]


class SearchTask(BaseTask):
    def __init__(self):
        super().__init__("search")

    def get_chain(
        self,
        target: Literal["name", "image", "image_name"],
        good: GoodDumped,
        limit: int = 100,
        threshold: float = None,
    ):
        embed_task: AsyncResult = current_app.send_task(
            f"ml.tasks.process_{target}",
            args=[good],
            queue=f"ml",
        )

        embedding: GoodEmbeddingDumped = embed_task.get()

        search_task = current_app.send_task(
            f"storage.tasks.search.{self.target}",
            kwargs={"limit": limit, "threshold": threshold},
            queue="storage",
        )
        ids = search_task.get()
        goods = GoodRepository().get_by_ids(ids)
        good_dumps: list[GoodDumped] = [
            Good.from_orm(good).model_dump() for good in goods
        ]

        return good_dumps


class SearchTask(BaseTask):
    def __init__(self):
        super().__init__("search")

    def run(
        self, good: GoodDumped, *, limit: int = 100, threshold: float = None
    ) -> list[GoodDumped]:
        good_model = Good.model_validate(good)
        assert good_model.id is not None

        has_name = good_model.name is not None
        has_image = good_model.image is not None

        target: Literal["name", "image", "name_image"] = None
        if has_name and has_image:
            target = "name_image"
        elif has_name:
            target = "name"
        elif has_image:
            target = "image"
        else:
            raise ValueError("Good must have name or image")

        task = SearchByXXXTask(target).signature(
            args=[good],
            kwargs={"limit": limit, "threshold": threshold},
            queue="agent",
        )
        return get_task(task)


def get_tasks():
    return [
        SearchByXXXTask("name"),
        SearchByXXXTask("image"),
        SearchByXXXTask("name_image"),
        SearchTask(),
    ]
