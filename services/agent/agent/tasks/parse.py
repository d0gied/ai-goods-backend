from typing import Literal

from celery import chain, chunks, group, signature
from celery.result import AsyncResult
from global_modules.db.models.good import Good as GoodORM
from global_modules.db.repositories import GoodRepository
from global_modules.db.schemas import UpdateGoodEmbeddingsSchema
from global_modules.db.services.good import GoodService
from global_modules.db.uow import UnitOfWork
from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodDumped, GoodEmbedding, GoodEmbeddingDumped

from .base import BaseTask


class AddGoodsToDBAndFilterTask(BaseTask):
    def __init__(self):
        super().__init__("add_to_db")

    def run(self, goods: list[GoodDumped], force_reprocess: bool = False):
        good_service = GoodService()
        good_models = [Good.model_validate(good) for good in goods]

        for good in good_models:
            if good.source_id is None:
                good.source_id = str(good.id)

        existing_goods = good_service.get_by_source_ids(
            source=good_models[0].source,
            ids=[good.source_id for good in good_models],
        )

        db_goods = {
            good.source_id: good
            for good in existing_goods
            if good.source_id is not None
        }

        schemas = []
        needs_processing = []
        for good in good_models:
            db_good: Good = db_goods.get(good.source_id, None)

            if db_good is None:
                schemas.append(good.to_add_schema())
                needs_processing.append(good)
            else:
                if force_reprocess or db_good.is_processed is False:
                    needs_processing.append(good)

        # add new goods to db and update dict with new goods
        good_models = good_service.add_many(schemas)
        db_goods.update({good.source_id: good for good in good_models})

        # get valid good ids from db
        for good in needs_processing:
            good.id = db_goods[good.source_id].id

        # dump goods
        needs_processing = [good.model_dump() for good in needs_processing]

        return needs_processing


class AddGoodEmbeddingsToDBTask(BaseTask):
    def __init__(self):
        super().__init__("add_embeddings_to_db")
        self.time_limit = 10  # 5 seconds
        self.soft_time_limit = 5  # 5 seconds
        self.max_retries = 3

    def run(
        self,
        good: GoodEmbeddingDumped,
        target: Literal["image", "name", "name_image"],
    ):
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
        with UnitOfWork() as uow:
            uow.goods.update(good_embedding.id, matches[target])
        return good


class EmbedAndSaveGoodsTask(BaseTask):
    def __init__(self):
        super().__init__(f"embed_and_save_goods")
        self.time_limit = 10  # 10 seconds
        self.soft_time_limit = 10  # 10 seconds
        self.max_retries = 3

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

    def run(
        self,
        goods: list[GoodDumped],
        target: Literal["name", "image", "name_image", "all"] = "all",
    ):
        embed_tasks = []
        for good in goods:
            good_model = Good.model_validate(good)
            has_image = good_model.images is not None and len(good_model.images) > 0
            has_name = good_model.name is not None and len(good_model.name) > 0

            if target == "all":
                if has_image and has_name:
                    embed_tasks.append(self.get_chain(good, "name_image"))
                if has_image:
                    embed_tasks.append(self.get_chain(good, "image"))
                if has_name:
                    embed_tasks.append(self.get_chain(good, "name"))
            else:
                if target == "image" and has_image:
                    embed_tasks.append(self.get_chain(good, "image"))
                if target == "name" and has_name:
                    embed_tasks.append(self.get_chain(good, "name"))
                if target == "name_image" and has_image and has_name:
                    embed_tasks.append(self.get_chain(good, "name_image"))

        return group(embed_tasks)()


class ReEmbedAllGoodsTask(BaseTask):
    def __init__(self):
        super().__init__(f"reembed_all_goods")
        # self.time_limit = 10  # 10 seconds
        # self.soft_time_limit = 10  # 10 seconds
        # self.max_retries = 3

    def run(self, target: Literal["name", "image", "name_image", "all"], **kwargs):
        with UnitOfWork() as uow:
            goods = uow.goods.get_all()
            goods = [Good.from_orm(good).model_dump() for good in goods]

        return EmbedAndSaveGoodsTask().run(goods, target=target)


class ParseTask(BaseTask):
    def __init__(
        self,
        source: Literal["wildberries", "alibaba", "ozon"],
        force_reprocess: bool = False,
    ):
        super().__init__(f"parse.{source}")
        self.source = source

    def run(
        self,
        request: str,
        limit: int = 100,
        chunk_size: int = 10,
        do_embed: bool = True,
    ):
        parse_task = signature(
            f"parser.tasks.get_goods.{self.source}",
            args=[request],
            kwargs={"limit": limit},
            queue="parser",
        )
        add_to_db_task = AddGoodsToDBAndFilterTask().signature(queue="agent")
        embed_and_save_task = EmbedAndSaveGoodsTask().signature(queue="agent")
        if do_embed:
            return chain(parse_task, add_to_db_task, embed_and_save_task)()
        else:
            return chain(parse_task, add_to_db_task)()


def get_tasks() -> BaseTask:
    """Get all tasks"""
    return [
        ParseTask("wildberries"),
        ParseTask("alibaba"),
        ParseTask("ozon"),
        AddGoodEmbeddingsToDBTask(),
        AddGoodsToDBAndFilterTask(),
        EmbedAndSaveGoodsTask(),
        ReEmbedAllGoodsTask(),
    ]
