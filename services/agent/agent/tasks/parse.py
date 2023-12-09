from typing import Literal

from celery import current_app
from celery.result import AsyncResult
from global_modules.db.repositories import GoodRepository
from global_modules.db.schemas import UpdateGoodEmbeddingsSchema
from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodDumped, GoodEmbedding, GoodEmbeddingDumped

from .base import BaseTask


class EmbedAndSaveImageTask(BaseTask):
    """Embed and save"""

    def __init__(self):
        super().__init__("embed_and_save.image")

    def run(self, good: GoodDumped):
        good_model = Good.model_validate(good)
        assert good_model.id is not None  # noqa: S101

        embed_task = current_app.send_task(
            "ml.tasks.process_image",
            args=[good],
            queue=CeleryQueue.ML_IMAGE,
        )

        embedding: GoodEmbeddingDumped = embed_task.get()
        embed_model = GoodEmbedding.model_validate(embedding)
        update_schema = UpdateGoodEmbeddingsSchema(
            image_embedding=embed_model.image_embedding,
        )
        GoodRepository().update(good_model.id, update_schema)

        save_task = current_app.send_task(
            "storage.tasks.add.image",
            args=[embedding],
            queue=CeleryQueue.STORAGE_IMAGE,
        )
        save_task.get()


class EmbedAndSaveNameTask(BaseTask):
    """Embed and save"""

    def __init__(self):
        super().__init__("embed_and_save.name")

    def run(self, good: GoodDumped):
        good_model = Good.model_validate(good)
        assert good_model.id is not None  # noqa: S101

        embed_task = current_app.send_task(
            "ml.tasks.process_name",
            args=[good],
            queue=CeleryQueue.ML_NAME,
        )

        embedding: GoodEmbeddingDumped = embed_task.get()
        embed_model = GoodEmbedding.model_validate(embedding)
        update_schema = UpdateGoodEmbeddingsSchema(
            name_embedding=embed_model.name_embedding,
        )
        GoodRepository().update(good_model.id, update_schema)

        save_task = current_app.send_task(
            "storage.tasks.add.name",
            args=[embedding],
            queue=CeleryQueue.STORAGE_NAME,
        )
        save_task.get()


class EmbedAndSaveNameImageTask(BaseTask):
    """Embed and save"""

    def __init__(self):
        super().__init__("embed_and_save.name_image")

    def run(self, good: GoodDumped):
        good_model = Good.model_validate(good)
        assert good_model.id is not None  # noqa: S101

        embed_task = current_app.send_task(
            "ml.tasks.process_name_image",
            args=[good],
            queue=CeleryQueue.ML_NAME_IMAGE,
        )

        embedding: GoodEmbeddingDumped = embed_task.get()
        embed_model = GoodEmbedding.model_validate(embedding)
        update_schema = UpdateGoodEmbeddingsSchema(
            name_image_embedding=embed_model.name_image_embedding,
        )
        GoodRepository().update(good_model.id, update_schema)

        save_task = current_app.send_task(
            "storage.tasks.add.name_image",
            args=[embedding],
            queue=CeleryQueue.STORAGE_NAME_IMAGE,
        )
        save_task.get()


class ParseTask(BaseTask):
    """Parse wildberries"""

    def __init__(self, name: Literal["wildberries", "alibaba", "ozon"]):
        super().__init__(f"parse.{name}")
        self.source = name

    def run(self, request: str, limit: int = 100):
        """Run task"""
        task_name = f"parser.tasks.get_goods.{self.source}"
        parsing_task: AsyncResult = current_app.send_task(
            task_name,
            args=[request],
            kwargs={"limit": limit},
            queue=f"parse.{self.source}",
        )

        goods: list[GoodDumped] = parsing_task.get()

        for good in goods:
            good_model = Good.model_validate(good)
            add_schema = good_model.to_add_schema()
            db_good = GoodRepository().add(add_schema)
            good["id"] = db_good.id

        image_tasks = []
        name_tasks = []
        name_image_tasks = []
        for good in goods:
            image_tasks.append(
                EmbedAndSaveImageTask().apply_async(
                    args=[good],
                )
            )
            name_tasks.append(
                EmbedAndSaveNameTask().apply_async(
                    args=[good],
                )
            )
            name_image_tasks.append(
                EmbedAndSaveNameImageTask().apply_async(
                    args=[good],
                )
            )

        for task in image_tasks:
            task.get()
        for task in name_tasks:
            task.get()
        for task in name_image_tasks:
            task.get()

        return


def get_tasks() -> BaseTask:
    """Get all tasks"""
    return [
        ParseTask("wildberries"),
        ParseTask("alibaba"),
        ParseTask("ozon"),
    ]
