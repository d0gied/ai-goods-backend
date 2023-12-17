from ..models import GoodEmbedding
from ..storage import Storage, get_storage
from .base import BaseTask


class AddTask(BaseTask):
    """Add goos by embedding"""

    def __init__(self, name: str):
        super().__init__(f"add.{name}")

    def run(self, goods: list[dict] | dict):
        """Run task"""
        if isinstance(goods, dict):
            goods = [goods]
        goods = [GoodEmbedding.model_validate(good) for good in goods]

        storage = get_storage()
        self.add(storage, goods)
        storage.save()

    def add(self, storage: Storage, goods: list[GoodEmbedding]):
        """Add goods to storage"""
        raise NotImplementedError("Subclasses must implement this method")


class AddByNameTask(AddTask):
    """Add goods by name"""

    def __init__(self):
        super().__init__("name")

    def add(self, storage: Storage, goods: list[GoodEmbedding]):
        """Add goods to storage"""
        storage.add_by_name(goods)


class AddByImageTask(AddTask):
    """Add goods by image"""

    def __init__(self):
        super().__init__("image")

    def add(self, storage: Storage, goods: list[GoodEmbedding]):
        """Add goods to storage"""
        storage.add_by_image(goods)


class AddByNameImageTask(AddTask):
    """Add goods by name and image"""

    def __init__(self):
        super().__init__("name_image")

    def add(self, storage: Storage, goods: list[GoodEmbedding]):
        """Add goods to storage"""
        storage.add_by_name_image(goods)


def get_tasks() -> list[BaseTask]:
    return [
        AddByNameTask(),
        AddByImageTask(),
        AddByNameImageTask(),
    ]
