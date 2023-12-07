from abc import ABC, abstractmethod
from typing import Any

class Embedding(ABC):
    size: int = 512
    
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_embedding(self, data: Any, **kwargs) -> list[float]:
        """Get embedding from data"""
        pass
    
    @abstractmethod
    def get_distance(self, embedding1: list[float], embedding2: list[float], **kwargs) -> float:
        """Get distance between embeddings"""
        pass
    
    @abstractmethod
    def get_similar(self, embedding: list[float], embeddings: list[list[float]], **kwargs) -> list[int]:
        """Get similar embeddings"""
        pass
    
    @abstractmethod
    def get_similarity(self, embedding1: list[float], embedding2: list[float], **kwargs) -> float:
        """Get similarity between embeddings"""
        pass