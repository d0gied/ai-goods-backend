from .base import BaseTask
from ..models import Good

class AddGoodsTask(BaseTask):
    """ Add goods task """
    def __init__(self):
        super().__init__(name="add_goods")

    def run(self, goods: list[dict], **kwargs):
        """ Run the task """
        goods = [Good(**good) for good in goods]
        
        #TODO: add goods to vector storage
        
        raise NotImplementedError("Add goods to vector storage")