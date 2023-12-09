import celery


class BaseTask(celery.Task):
    """Base task"""

    queue: str = "agent"

    def __init__(self, name: str):
        super().__init__()
        self.name = f"agent.tasks.{name}"
