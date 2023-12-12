import time
from typing import Literal

from celery import chain, current_app, signature
from celery.result import AsyncResult
from global_modules.db.repositories import GoodRepository
from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodDumped, GoodEmbedding, GoodEmbeddingDumped

from .base import BaseTask


class LoadGoodsFromDBByIdsTask(BaseTask):
    def __init__(self):
        super().__init__("load_goods_from_db_by_ids")

    def run(self, ids: list[int]) -> list[GoodDumped]:
        goods = GoodRepository().get_by_ids(ids)
        return [Good.from_orm(good).model_dump() for good in goods]


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
        embed_task = signature(
            f"ml.tasks.process_{target}",
            args=[good],
            queue=f"ml",
        )
        search_task = signature(
            f"storage.tasks.search.{self.target}",
            kwargs={"limit": limit, "threshold": threshold},
            queue="storage",
        )
        db_task = LoadGoodsFromDBByIdsTask().signature(queue="agent")

        return chain(embed_task, search_task, db_task)

    def run(
        self,
        good: GoodDumped,
        *,
        limit: int = 100,
        threshold: float = None,
    ) -> list[GoodEmbeddingDumped]:
        good_model = Good.model_validate(good)
        has_image = good_model.images is not None and len(good_model.images) > 0
        has_name = good_model.name is not None and len(good_model.name) > 0

        target: str = None
        if has_image and has_name:
            target = "image_name"
        elif has_image:
            target = "image"
        elif has_name:
            target = "name"
        else:
            raise ValueError("Good has no name or image")

        return self.get_chain(target, good, limit, threshold)()


def get_tasks():
    return [
        SearchTask(),
        LoadGoodsFromDBByIdsTask(),
    ]
