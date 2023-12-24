from functools import lru_cache

from .base import Embedding
from ..models.text import MatchingModel, get_matching_model

class TextEmbedding(Embedding):
    """Text embedding"""

    size: int = 768

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_embedding(self, data: str, **kwargs) -> list[float]:
        """Get embedding from data"""

        model = get_matching_model()
        emb = model.run(data)

        return emb

    def get_embeddings(self, data: list[str], **kwargs) -> list[list[float]]:
        """Get embeddings from data"""
        embeddings = []
        for item in data:
            embeddings.append(self.get_embedding(item, **kwargs))
        return embeddings

    def get_distance(
        self, embedding1: list[float], embedding2: list[float], **kwargs
    ) -> float:
        """Get distance between embeddings"""
        pass

    def get_similar(
        self, embedding: list[float], embeddings: list[list[float]], **kwargs
    ) -> list[int]:
        """Get similar embeddings"""
        pass

    def get_similarity(
        self, embedding1: list[float], embedding2: list[float], **kwargs
    ) -> float:
        """Get similarity between embeddings"""
        pass


@lru_cache
def get_embeddings() -> TextEmbedding:
    """Get embeddings model"""
    return TextEmbedding()
