from .process_image import get_tasks as get_image_tasks
from .process_name import get_tasks as get_name_tasks
from .base import BaseTask

def get_tasks() -> list[BaseTask]:
    return [
        *get_image_tasks(),
        *get_name_tasks(),
    ]
    
