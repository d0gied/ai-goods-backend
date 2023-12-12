from typing import Literal

from celery import chain, group, signature
from celery.result import AsyncResult
from global_modules.db.repositories import GoodRepository
from global_modules.db.schemas import UpdateGoodEmbeddingsSchema
from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodDumped, GoodEmbedding, GoodEmbeddingDumped

from .base import BaseTask


class AddGoodsToDBAndFilterTask(BaseTask):
    def __init__(self):
        super().__init__("add_to_db")

    def run(self, goods: list[GoodDumped], force_reprocess: bool = False):
        good_repository = GoodRepository()
        good_models = [Good.model_validate(good) for good in goods]

        for good in good_models:
            if good.source_id is None:
                good.source_id = str(good.id)

        existing_goods = good_repository.get_by_source_ids(
            source=good_models[0].source,
            ids=[good.source_id for good in good_models],
        )

        existing_ids = set([good.source_id for good in existing_goods])
        schemas = []
        result_goods = []
        for good in good_models:
            # check if good already exists
            if good.source_id not in existing_ids:
                schemas.append(good.to_add_schema())
                result_goods.append(good.model_dump())
            elif force_reprocess:
                # TODO: add reprocess logic
                # NOTE: needs to clear embeddings from vector storage
                # result_goods.append(good.model_dump())
                pass

        good_models = good_repository.add_many(schemas)
        for good_model, good in zip(good_models, result_goods):
            good["id"] = good_model.id
        return result_goods


class AddGoodEmbeddingsToDBTask(BaseTask):
    def __init__(self):
        super().__init__("add_embeddings_to_db")

    def run(
        self,
        good: GoodEmbeddingDumped,
        target: Literal["image", "name", "name_image"],
    ):
        good_repository = GoodRepository()
        good_embedding = GoodEmbedding.model_validate(good)
        matches = {
            "image": UpdateGoodEmbeddingsSchema(
                image_embedding=good_embedding.vector, is_processed=True
            ),
            "name": UpdateGoodEmbeddingsSchema(
                name_embedding=good_embedding.vector, is_processed=True
            ),
            "name_image": UpdateGoodEmbeddingsSchema(
                name_image_embedding=good_embedding.vector, is_processed=True
            ),
        }
        good_repository.update(good_embedding.id, matches[target])
        return good


class EmbedAndSaveGoodsTask(BaseTask):
    def __init__(self):
        super().__init__(f"embed_and_save_goods")

    def get_chain(
        self, good: GoodDumped, target: Literal["image", "name", "name_image"]
    ):
        embed_task = signature(
            f"ml.tasks.process_{target}",
            args=[good],
            queue="ml",
        )
        db_task = AddGoodEmbeddingsToDBTask().s(target=target).set(queue="agent")
        storage_task = signature(
            f"storage.tasks.add.{target}",
            queue="storage",
        )

        return chain(embed_task, db_task, storage_task)

    def run(self, goods: list[GoodDumped]):
        embed_tasks = []
        for good in goods:
            good_model = Good.model_validate(good)
            has_image = good_model.images is not None and len(good_model.images) > 0
            has_name = good_model.name is not None and len(good_model.name) > 0

            if has_image and has_name:
                embed_tasks.append(self.get_chain(good, "name_image"))
            if has_image:
                embed_tasks.append(self.get_chain(good, "image"))
            if has_name:
                embed_tasks.append(self.get_chain(good, "name"))
        return group(embed_tasks)()


class ParseTask(BaseTask):
    def __init__(
        self,
        source: Literal["wildberries", "alibaba", "ozon"],
        force_reprocess: bool = False,
    ):
        super().__init__(f"parse.{source}")
        self.source = source

    def run(self, request: str, limit: int = 100):
        parse_task = signature(
            f"parser.tasks.get_goods.{self.source}",
            args=[request],
            kwargs={"limit": limit},
            queue="parser",
        )
        add_to_db_task = AddGoodsToDBAndFilterTask().signature(queue="agent")
        embed_and_save_task = EmbedAndSaveGoodsTask().signature(queue="agent")

        return chain(parse_task, add_to_db_task, embed_and_save_task)()


def get_tasks() -> BaseTask:
    """Get all tasks"""
    return [
        ParseTask("wildberries"),
        ParseTask("alibaba"),
        ParseTask("ozon"),
        AddGoodEmbeddingsToDBTask(),
        AddGoodsToDBAndFilterTask(),
        EmbedAndSaveGoodsTask(),
    ]
