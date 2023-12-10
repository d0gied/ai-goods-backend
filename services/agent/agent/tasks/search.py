from typing import Literal

from celery import current_app
from celery.result import AsyncResult
from global_modules.db.repositories import GoodRepository
from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodDumped, GoodEmbedding, GoodEmbeddingDumped

from .base import BaseTask


class SearchByXXXTask(BaseTask):
    def __init__(self, name: Literal["name", "image", "name_image"]):
        super().__init__("search_by_{}".format(name))
        self.target = name

    def run(
        self, good: GoodDumped, *, limit: int = 100, threshold: float = None
    ) -> list[GoodDumped]:
        good_model = Good.model_validate(good)

        embed_task: AsyncResult = current_app.send_task(
            f"ml.tasks.process_{self.target}",
            args=[good],
            queue=f"ml.{self.target}",
        )

        embedding: GoodEmbeddingDumped = embed_task.get()

        search_task = current_app.send_task(
            f"storage.tasks.search.{self.target}",
            args=[embedding],
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

        SearchByXXXTask(target)

        task = SearchByXXXTask(target).apply_async(
            args=[good],
            kwargs={"limit": limit, "threshold": threshold},
            queue=SearchByXXXTask.queue,
        )
        return task.get()


def get_tasks():
    return [
        SearchByXXXTask("name"),
        SearchByXXXTask("image"),
        SearchByXXXTask("name_image"),
        SearchTask(),
    ]
