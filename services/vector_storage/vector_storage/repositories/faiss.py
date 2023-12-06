from vector_storage.models import Good, GoodEmbedding
from .base import BaseRepository
from ..models import GoodEmbedding
from faiss import IndexFlatL2, IndexIDMap, write_index, read_index
import numpy as np
from pathlib import Path

class FaissRepository(BaseRepository):
    """ Faiss repository """
    def __init__(self, path: str | Path, size: int = 512):
        super().__init__(path, size)
        self.faiss = IndexIDMap(IndexFlatL2(size))
        
    def add(self, embeddings: list[GoodEmbedding]):
        """ Add embeddings to repository """
        vectors  = [embedding.vector for embedding in embeddings]
        ids = [embedding.id for embedding in embeddings]
        self.faiss.add_with_ids(np.array(vectors), np.array(ids, dtype=np.int64))
        
    def delete(self, ids: list[int]):
        """ Delete embeddings from repository """
        self.faiss.remove_ids(np.array(ids, dtype=np.int64))
        
    def get(self, id: str) -> GoodEmbedding:
        """ Get embedding from repository """
        vector = self.faiss.reconstruct(int(id))
        return GoodEmbedding(id=id, vector=vector)
    
    def search(self, embedding: GoodEmbedding, k: int = 10, threshold: float = None) -> list[int]:
        """ Search for similar embeddings """
        vectors = np.array([embedding.vector])
        distances, ids = self.faiss.search(vectors, k)
        
        if threshold is None:
            return ids[0].tolist()
        
        result_ids = []
        for i, distance in enumerate(distances[0]):
            if distance < threshold:
                result_ids.append(ids[0][i].item())
        return result_ids
    
    def save(self):
        """ Save repository """
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        write_index(self.faiss, str(self.path))
        
    def load(self) -> bool:
        """ Load repository 
        
        Returns:
            bool: True if repository exists
        """
        if self.path.exists():
            self.faiss = read_index(str(self.path))
            return True
        return False