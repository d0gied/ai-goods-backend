from vector_storage.models import Good
from .base import BaseRepository
from ..models import Good
from langchain.vectorstores.faiss import FAISS 
from langchain.docstore.document import Document


class FaissRepository(BaseRepository):
    """ Faiss repository """
    def __init__(self):
        super().__init__()
        
        self.image_storage = FAISS()
        self.name_storage = FAISS()
        self.image_name_storage = FAISS()
        
    def add_goods(self, goods: list[Good]):
        return super().add_goods(goods)