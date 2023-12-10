from global_modules.models import Good, GoodEmbedding

from ..base import BaseTask


class BaseMLTask(BaseTask):
    """Base task class"""

    queue = "ml"

    def __init__(self, name: str, *args, **kwargs):
        super().__init__("ml", name)

    def run(self, *args, **kwargs):
        ...


class BaseGoodToEmbeddingTask(BaseMLTask):
    """Base task class"""

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name)

    def run(self, good: dict, *args, **kwargs) -> dict:
        pass
