from .add import get_tasks as get_add_tasks
from .delete import get_tasks as get_delete_tasks
from .search import get_tasks as get_search_tasks
from celery import Celery

def get_tasks():
    return [
        *get_add_tasks(),
        *get_delete_tasks(),
        *get_search_tasks(),
    ]
    
def register_tasks(celery: Celery):
    """ Register tasks """
    for task in get_tasks():
        celery.register_task(task)