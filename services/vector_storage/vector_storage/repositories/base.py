from abc import ABC, abstractmethod
from pydantic import BaseModel
from ..models import Good

class BaseRepository(ABC):
    """ Base repository """
    @abstractmethod
    def add_goods(self, goods: list[Good]):
        """ Add goods to vector storage """
        pass

    @abstractmethod
    def get_goods(self, good: Good, limit: int = 10) -> list[Good]:
        """ Get goods from vector storage """
        pass
    
    def remove_goods(self, goods: list[Good]):
        """ Remove goods from vector storage """
        pass