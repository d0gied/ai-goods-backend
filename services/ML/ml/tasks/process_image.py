from .base import BaseGoodToEmbeddingTask, BaseTask
from ..embeddings.image import get_embeddings
from global_modules.models import Good, GoodEmbedding

class ProcessImageTask(BaseGoodToEmbeddingTask):
    """Process image task"""

    def __init__(self):
        super().__init__("process_image")
    
    def task(self, good: Good) -> GoodEmbedding:
        """Run task"""
        image_embeddings = get_embeddings()
        vector = image_embeddings.get_embedding(good.images[0])
        good_embedding = GoodEmbedding(id=good.id, vector=vector)
        return good_embedding

def get_tasks() -> list[BaseTask]:
    return [
        ProcessImageTask(),
    ]