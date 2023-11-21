from .base import Parser
from ..models import Good

class AlibabaParser(Parser):
    """ Alibaba parser """
        
    def get_goods(self, request: str, *, limit: int = 100, **kwargs) -> list[Good]:
        # TODO: Implement this method
        raise NotImplementedError
    
    def get_good(self, good_id: str, **kwargs) -> Good:
        # TODO: Implement this method
        raise NotImplementedError



