import celery


class BaseTask(celery.Task):
    def __init__(self, name: str):
        super().__init__()
