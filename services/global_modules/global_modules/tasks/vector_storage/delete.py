from abc import ABC, abstractmethod

from ...models import GoodEmbeddingDumped
from .base import BaseStorageTask


class DeleteTask(BaseStorageTask, ABC):
    name = "delete"

    @abstractmethod
    def run(self, good: GoodEmbeddingDumped):
        """Run task"""


class DeleteByNameTask(DeleteTask, ABC):
    name = "name"


class DeleteByImageTask(DeleteTask, ABC):
    name = "image"


class DeleteByNameImageTask(DeleteTask, ABC):
    name = "name_image"
