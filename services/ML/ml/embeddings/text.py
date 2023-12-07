from .base import Embedding
from functools import lru_cache

class TextEmbedding(Embedding):
    """ Text embedding """
    size: int = 512
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_embedding(self, data: str, **kwargs) -> list[float]:
        """Get embedding from data"""
        # TODO: needs to be implemented
        pass
        return [0] * self.size
    
    def get_distance(self, embedding1: list[float], embedding2: list[float], **kwargs) -> float:
        """Get distance between embeddings"""
        pass
    def get_similar(self, embedding: list[float], embeddings: list[list[float]], **kwargs) -> list[int]:
        """Get similar embeddings"""
        pass

    def get_similarity(self, embedding1: list[float], embedding2: list[float], **kwargs) -> float:
        """Get similarity between embeddings"""
        pass

@lru_cache
def get_embeddings() -> TextEmbedding:
    """ Get embeddings model """
    return TextEmbedding()