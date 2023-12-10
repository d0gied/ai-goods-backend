import celery
from typing_extensions import deprecated

from .meta import RecurentTaskNamingMixin


@deprecated("Class is under development and should not be used")
class BaseTask(celery.Task, metaclass=RecurentTaskNamingMixin):
    queue = "default"
    name = "tasks"

    @deprecated("Class is under development and should not be used")
    def __init__(self):
        super().__init__()
        # to prevent renaming in celery Task building
        self.name = self.__class__.name
