from .base import Embedding
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from functools import lru_cache

class ImageEmbedding(Embedding):
    """ Image embedding """
    size: int = 512
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @staticmethod
    def load_image(url: str) -> np.ndarray:
        """ Load image from URL """

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Can't load image from {url}")
        return np.array(Image.open(BytesIO(response.content)))
        
    
    def get_embedding(self, data: str, **kwargs) -> list[float]:
        """Get embedding from data"""
        image = self.load_image(data)
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
def get_embeddings() -> ImageEmbedding:
    """ Get embeddings model """
    return ImageEmbedding()