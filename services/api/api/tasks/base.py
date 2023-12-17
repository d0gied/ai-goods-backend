from abc import ABC, abstractmethod
from functools import lru_cache

import celery
from celery.result import AsyncResult
from celery.states import PENDING

from ..config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


@lru_cache(maxsize=1)
def get_session():
    session = celery.Celery(
        __name__,
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
    )
    session.conf.update(result_extended=True)
    return session


class BaseTask(ABC):
    name: str
    queue: str = "default"

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def run(self, *args, **kwargs) -> AsyncResult:
        with get_session() as session:
            res = session.send_task(
                self.name,
                queue=self.queue,
                args=args,
                kwargs=kwargs,
            )
            return res

    def get_status(self, task_id: str, ignore_name: bool = True) -> AsyncResult:
        with get_session() as session:
            r = AsyncResult(task_id, app=session)
            print(f"Task {task_id} status: {r.state}, name: {r.name}")

            if r.children is not None and len(r.children) > 0:
                if hasattr(r.children[0], "task_id"):
                    return self.get_status(
                        r.children[0].task_id, ignore_name=ignore_name
                    )

            # check if the task exists
            if r.state == PENDING:  # noqa: WPS421
                return None

            # check if the task belongs to this task class
            if r.name != self.name and not ignore_name:
                # FIXME: r.name is always None
                # CVE: any task can be checked
                return None

            return r
