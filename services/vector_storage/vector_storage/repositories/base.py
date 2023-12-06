from abc import ABC, abstractmethod
from pydantic import BaseModel
from ..models import GoodEmbedding
from pathlib import Path


class BaseRepository(ABC):
    """Base repository"""
    
    def __init__(self, path: str | Path, size: int = 512):
        super().__init__()
        if isinstance(path, str):
            self.path = Path(path)
        else:
            self.path = path
        self.path: Path
        self.size = size

    @abstractmethod
    def add(self, embeddings: list[GoodEmbedding]):
        """Add embeddings to repository"""
        pass

    @abstractmethod
    def get(self, id: str) -> GoodEmbedding:
        """Get embedding from repository"""
        pass

    @abstractmethod
    def delete(self, ids: list[int]):
        """Delete embedding from repository"""
        pass

    @abstractmethod
    def search(
        self, embedding: GoodEmbedding, k: int = 10, threshold: float = None
    ) -> list[int]:
        """Search for similar embeddings"""
        pass

    @abstractmethod
    def save(self):
        """Save repository"""
        pass

    @abstractmethod
    def load(self) -> bool:
        """ Load repository 
        
        Returns:
            bool: True if repository exists
        """
        pass
