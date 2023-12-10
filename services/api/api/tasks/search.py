from global_modules.models import Good

from .base import BaseTask


class SearchTask(BaseTask):
    name = "agent.tasks.search"
    queue = "agent"

    def run(
        self, good: Good, *, limit: int = 100, threshold: float = None, **kwargs
    ) -> None:
        super().run(good.model_dump(), limit=100, threshold=threshold, **kwargs)
