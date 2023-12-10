from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodEmbedding

from ..embeddings.text import get_embeddings
from .base import BaseGoodToEmbeddingTask, BaseTask


class ProcessNameTask(BaseGoodToEmbeddingTask):
    """Process name task"""

    queue = CeleryQueue.ML_NAME.value

    def __init__(self):
        super().__init__("process_name")

    def task(self, good: Good) -> GoodEmbedding:
        """Run task"""
        text_embeddings = get_embeddings()
        vector = text_embeddings.get_embedding(good.name)
        good_embedding = GoodEmbedding(id=good.id, vector=vector)
        return good_embedding


def get_tasks() -> list[BaseTask]:
    return [
        ProcessNameTask(),
    ]
