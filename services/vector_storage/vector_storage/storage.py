from functools import lru_cache
from pathlib import Path
from typing import Type

from .models import GoodEmbedding
from .repositories.base import BaseRepository
from .repositories.faiss import FaissRepository


class Storage:
    def __init__(
        self,
        name_repo: BaseRepository,
        image_repo: BaseRepository,
        name_image_repo: BaseRepository,
    ) -> None:
        self.name_repo = name_repo
        self.image_repo = image_repo
        self.name_image_repo = name_image_repo

    def add_by_name(self, names: list[GoodEmbedding]):
        self.name_repo.add(names)

    def add_by_image(self, images: list[GoodEmbedding]):
        self.image_repo.add(images)

    def add_by_name_image(self, names_images: list[GoodEmbedding]):
        self.name_image_repo.add(names_images)

    def delete_by_name(self, ids: list[int]):
        self.name_repo.delete(ids)

    def delete_by_image(self, ids: list[int]):
        self.image_repo.delete(ids)

    def delete_by_name_image(self, ids: list[int]):
        self.name_image_repo.delete(ids)

    def search_by_name(
        self, name: GoodEmbedding, k: int = 10, threshold: float = None
    ) -> list[int]:
        return self.name_repo.search(name, k, threshold)

    def search_by_image(
        self, image: GoodEmbedding, k: int = 10, threshold: float = None
    ) -> list[int]:
        return self.image_repo.search(image, k, threshold)

    def search_by_name_image(
        self, name_image: GoodEmbedding, k: int = 10, threshold: float = None
    ) -> list[int]:
        return self.name_image_repo.search(name_image, k, threshold)

    def save(self):
        self.name_repo.save()
        self.image_repo.save()
        self.name_image_repo.save()

    def load(self):
        self.name_repo.load()
        self.image_repo.load()
        self.name_image_repo.load()


@lru_cache(maxsize=1)
def get_storage(path: str | Path = "./storage") -> Storage:
    if isinstance(path, str):
        path = Path(path)

    return Storage(
        FaissRepository(path / "names.db", 512),
        FaissRepository(path / "images.db", 512),
        FaissRepository(path / "names_images.db", 512),
    )
