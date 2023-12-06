from .base import BaseTask
from ..storage import get_storage, Storage
from ..models import GoodEmbedding


class DeleteTask(BaseTask):
    """Delete goods by embedding"""

    def __init__(self, name: str):
        super().__init__(f"delete.{name}")

    def run(self, goods: list[dict]):
        """Run task"""
        goods = [GoodEmbedding.model_validate(good) for good in goods]

        storage = get_storage()
        self.delete(storage, goods)
        storage.save()

    def delete(self, storage: Storage, goods: list[GoodEmbedding]):
        """Delete goods from storage"""
        raise NotImplementedError("Subclasses must implement this method")


class DeleteByNameTask(DeleteTask):
    """Delete goods by name"""

    def __init__(self):
        super().__init__("name")

    def delete(self, storage: Storage, goods: list[GoodEmbedding]):
        """Delete goods from storage"""
        storage.delete_by_name(goods)


class DeleteByImageTask(DeleteTask):
    """Delete goods by image"""

    def __init__(self):
        super().__init__("image")

    def delete(self, storage: Storage, goods: list[GoodEmbedding]):
        """Delete goods from storage"""
        storage.delete_by_image(goods)


class DeleteByNameImageTask(DeleteTask):
    """Delete goods by name and image"""

    def __init__(self):
        super().__init__("name_image")

    def delete(self, storage: Storage, goods: list[GoodEmbedding]):
        """Delete goods from storage"""
        storage.delete_by_name_image(goods)


def get_tasks() -> list[BaseTask]:
    return [
        DeleteByNameTask(),
        DeleteByImageTask(),
        DeleteByNameImageTask(),
    ]
