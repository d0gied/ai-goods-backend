from abc import ABC, abstractmethod

from ...models import GoodEmbeddingDumped
from .base import BaseStorageTask


class AddTask(BaseStorageTask, ABC):
    name = "add"

    @abstractmethod
    def run(self, goods: list[GoodEmbeddingDumped]):
        """Run task"""
