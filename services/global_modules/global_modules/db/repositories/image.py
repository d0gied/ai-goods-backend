from ..models import Image
from ..schemas import AddImageSchema, UpdateImageSchema
from .base import SQLAlchemyRepository


class ImageRepository(SQLAlchemyRepository):
    model = Image

    def get(self, id: int) -> Image | None:
        return super().get(id)

    def get_all(self) -> list[Image]:
        return super().get_all()

    def add(self, schema: AddImageSchema) -> Image:
        return super().add(schema)

    def add_many(self, schemas: list[AddImageSchema]) -> list[Image]:
        return super().add_many(schemas)

    def update(self, id: int, schema: UpdateImageSchema) -> Image:
        return super().update(id, schema)

    def delete(self, id: int) -> Image:
        return super().delete(id)

    def get_by_ids(self, ids: list[int]) -> list[Image]:
        return super().get_by_ids(ids)
