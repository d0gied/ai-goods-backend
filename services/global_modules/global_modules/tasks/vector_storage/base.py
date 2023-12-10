from abc import ABC

from ..base import BaseTask


class BaseStorageTask(BaseTask, ABC):
    name = "storage"
