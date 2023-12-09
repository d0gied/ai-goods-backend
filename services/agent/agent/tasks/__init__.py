from .base import BaseTask
from .parse import get_tasks as get_parse_tasks


def get_tasks() -> list[BaseTask]:
    """Get all tasks"""
    return [
        *get_parse_tasks(),
    ]
