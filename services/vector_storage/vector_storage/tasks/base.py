import celery

class BaseTask(celery.Task):
    def __init__(self, name: str):
        super().__init__()
        self.name = f"storage.tasks.{name}"

    def run(self, *args, **kwargs):
        """Run the task"""
        raise NotImplementedError("Subclasses must implement this method")