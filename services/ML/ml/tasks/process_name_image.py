from global_modules.enums import CeleryQueue
from global_modules.models import Good, GoodEmbedding

from ..embeddings.name_image import get_embeddings
from .base import BaseGoodToEmbeddingTask, BaseTask


class ProcessNameImageTask(BaseGoodToEmbeddingTask):
    """Process image task"""

    queue = CeleryQueue.ML_NAME_IMAGE.value

    def __init__(self):
        super().__init__("process_name_image")

    def task(self, good: Good) -> GoodEmbedding:
        """Run task"""
        name_image_embeddings = get_embeddings()
        vector = name_image_embeddings.get_embedding((good.name, good.images[0]))
        good_embedding = GoodEmbedding(id=good.id, vector=vector)
        return good_embedding


def get_tasks() -> list[BaseTask]:
    return [
        ProcessNameImageTask(),
    ]
