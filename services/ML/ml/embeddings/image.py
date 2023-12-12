from functools import lru_cache
from io import BytesIO

import numpy as np
import requests
from PIL import Image

from ..models.image import MatchingModel, get_matching_model, normalize_image
from .base import Embedding


class ImageEmbedding(Embedding):
    """Image embedding"""

    size: int = 512

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def load_image(url: str) -> np.ndarray:
        """Load image from URL"""

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Can't load image from {url}")
        return np.array(Image.open(BytesIO(response.content)))

    def get_embedding(self, data: str, **kwargs) -> list[float]:
        """Get embedding from data"""
        image = self.load_image(data)

        image = normalize_image(image)

        model = get_matching_model()
        emb = model.run([image])[0]

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
def get_embeddings() -> ImageEmbedding:
    """Get embeddings model"""
    return ImageEmbedding()
