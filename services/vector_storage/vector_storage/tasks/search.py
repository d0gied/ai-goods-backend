from .base import BaseTask
from ..storage import get_storage, Storage
from ..models import GoodEmbedding


class SearchTask(BaseTask):
    """Search goods by embedding"""

    def __init__(self, name: str):
        super().__init__(f"search.{name}")

    def run(self, goods: list[dict]):
        """Run task"""
        goods = [GoodEmbedding.model_validate(good) for good in goods]

        storage = get_storage()
        self.search(storage, goods)
        storage.save()

    def search(self, storage: Storage, goods: list[GoodEmbedding]):
        """Search goods in storage"""
        raise NotImplementedError("Subclasses must implement this method")


class SearchByNameTask(SearchTask):
    """Search goods by name"""

    def __init__(self):
        super().__init__("name")

    def search(self, storage: Storage, goods: list[GoodEmbedding]):
        """Search goods in storage"""
        storage.search_by_name(goods)


class SearchByImageTask(SearchTask):
    """Search goods by image"""

    def __init__(self):
        super().__init__("image")

    def search(self, storage: Storage, goods: list[GoodEmbedding]):
        """Search goods in storage"""
        storage.search_by_image(goods)


class SearchByNameImageTask(SearchTask):
    """Search goods by name and image"""

    def __init__(self):
        super().__init__("name_image")

    def search(self, storage: Storage, goods: list[GoodEmbedding]):
        """Search goods in storage"""
        storage.search_by_name_image(goods)


def get_tasks() -> list[BaseTask]:
    return [
        SearchByNameTask(),
        SearchByImageTask(),
        SearchByNameImageTask(),
    ]
