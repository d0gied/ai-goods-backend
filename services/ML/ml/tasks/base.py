from celery import Task
from global_modules.models import Good, GoodEmbedding

class BaseTask(Task):
    """Base task class"""

    def __init__(self, name: str):
        super().__init__()
        self.name = f"ml.tasks.{name}"

    def run(self, *args, **kwargs):
        """Run task"""
        raise NotImplementedError("Subclasses must implement this method")
    
class BaseGoodToEmbeddingTask(BaseTask):
    """Base task class"""

    def __init__(self, name: str):
        super().__init__(name)

    def run(self, good: dict) -> dict:
        good = Good.model_validate(good)
        good_embedding = self.task(good)
        good_embedding_dict = good_embedding.model_dump()
        return good_embedding_dict

    def task(self, good: Good) -> GoodEmbedding:
        """Run task"""
        raise NotImplementedError("Subclasses must implement this method")