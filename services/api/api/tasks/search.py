from celery.result import AsyncResult
from global_modules.models import Good

from .base import BaseTask


class SearchTask(BaseTask):
    name = "agent.tasks.search"
    queue = "agent"

    def run(
        self, good: Good, *, limit: int = 100, threshold: float = None, **kwargs
    ) -> None:
        return super().run(
            good.model_dump(), limit=limit, threshold=threshold, **kwargs
        )

    # def get_status(self, task_id: str, ignore_name: bool = True) -> AsyncResult:
    #     task_status = super().get_status(task_id, ignore_name=ignore_name)
    #     if task_status is None:
    #         return None

    #     if task_status.status == "SUCCESS":  # get status of child task
    #         return super().get_status(task_status.result[0][0])
    #     return task_status
