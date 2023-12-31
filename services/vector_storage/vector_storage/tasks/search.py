from ..models import GoodEmbedding
from ..storage import Storage, get_storage
from .base import BaseTask


class SearchTask(BaseTask):
    """Search goods by embedding"""

    def __init__(self, name: str):
        super().__init__(f"search.{name}")

    def run(self, good: dict, limit: int = 100, threshold: float = None) -> list[dict]:
        """Run task"""
        good = GoodEmbedding.model_validate(good)

        storage = get_storage()
        return self.search(storage, good, limit=limit, threshold=threshold)

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
        return storage.search_by_name(good, k=limit, threshold=threshold)


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
        return storage.search_by_image(good, k=limit, threshold=threshold)


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
        return storage.search_by_name_image(good, k=limit, threshold=threshold)


def get_tasks() -> list[BaseTask]:
    return [
        SearchByNameTask(),
        SearchByImageTask(),
        SearchByNameImageTask(),
    ]
