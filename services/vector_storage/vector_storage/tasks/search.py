from ..models import GoodEmbedding
from ..storage import Storage, get_storage
from .base import BaseTask


class SearchTask(BaseTask):
    """Search goods by embedding"""

    def __init__(self, name: str):
        super().__init__(f"search.{name}")

    def run(self, good: dict) -> list[dict]:
        """Run task"""
        goods = [GoodEmbedding.model_validate(good) for good in goods]

        storage = get_storage()
        self.search(storage, goods)
        storage.save()

    def search(
        self,
        storage: Storage,
        good: GoodEmbedding,
        *,
        limit: int = 100,
        threshold: float = None,
    ):
        """Search goods in storage"""
        raise NotImplementedError("Subclasses must implement this method")


class SearchByNameTask(SearchTask):
    """Search goods by name"""

    def __init__(self):
        super().__init__("name")

    def search(
        self,
        storage: Storage,
        good: GoodEmbedding,
        *,
        limit: int = 100,
        threshold: float = None,
    ):
        """Search goods in storage"""
        storage.search_by_name(good, k=limit, threshold=threshold)


class SearchByImageTask(SearchTask):
    """Search goods by image"""

    def __init__(self):
        super().__init__("image")

    def search(
        self,
        storage: Storage,
        good: GoodEmbedding,
        *,
        limit: int = 100,
        threshold: float = None,
    ):
        """Search goods in storage"""
        storage.search_by_image(good, k=limit, threshold=threshold)


class SearchByNameImageTask(SearchTask):
    """Search goods by name and image"""

    def __init__(self):
        super().__init__("name_image")

    def search(
        self,
        storage: Storage,
        good: GoodEmbedding,
        *,
        limit: int = 100,
        threshold: float = None,  # TODO: add threshold in other levels
    ):
        """Search goods in storage"""
        storage.search_by_name_image(good, k=limit, threshold=threshold)


def get_tasks() -> list[BaseTask]:
    return [
        SearchByNameTask(),
        SearchByImageTask(),
        SearchByNameImageTask(),
    ]
