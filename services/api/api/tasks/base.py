from abc import ABC, abstractmethod

import celery
from celery.result import AsyncResult
from celery.states import PENDING

from ..config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


def get_session():
    return celery.Celery(
        __name__,
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
    )


class BaseTask(ABC):
    name: str
    queue: str = "default"

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def run(self, *args, **kwargs) -> AsyncResult:
        with get_session() as session:
            return session.send_task(
                self.name,
                queue=self.queue,
                args=args,
                kwargs=kwargs,
            )

    def get_status(self, task_id: str) -> AsyncResult:
        with get_session() as session:
            r = AsyncResult(task_id, app=session)
            # check if the task exists
            if r.state == PENDING:  # noqa: WPS421
                return None
            return r
