from .base import BaseTask
from .process_image import get_tasks as get_image_tasks
from .process_name import get_tasks as get_name_tasks
from .process_name_image import get_tasks as get_name_image_tasks


def get_tasks() -> list[BaseTask]:
    return [
        *get_image_tasks(),
        *get_name_tasks(),
        *get_name_image_tasks(),
    ]
