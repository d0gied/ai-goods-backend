from abc import ABC, abstractmethod

from ...models import GoodEmbeddingDumped
from .base import BaseStorageTask


class SearchTask(BaseStorageTask, ABC):
    name = "search"

    @abstractmethod
    def run(self, good: GoodEmbeddingDumped) -> list[GoodEmbeddingDumped]:
        """Run task"""


class SearchByNameTask(SearchTask, ABC):
    name = "name"


class SearchByImageTask(SearchTask, ABC):
    name = "image"


class SearchByNameImageTask(SearchTask, ABC):
    name = "name_image"
