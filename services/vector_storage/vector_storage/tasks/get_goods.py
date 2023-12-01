from .base import BaseTask
from ..models import Good

class GetGoodsTask(BaseTask):
    """ Get goods task """
    def __init__(self):
        super().__init__(name="get_goods")

    def run(self, good: dict, **kwargs):
        """ Run the task """
        good = Good(**good)
        
        