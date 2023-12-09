from typing import Union

from ..db import SessionLocal
from ..models import Good
from ..schemas import AddGoodSchema, UpdateGoodEmbeddingsSchema, UpdateGoodSchema
from .base import SQLAlchemyRepository


class GoodRepository(SQLAlchemyRepository):
    model = Good

    def get(self, id: int) -> Good | None:
        return super().get(id)

    def get_all(self) -> list[Good]:
        return super().get_all()

    def add(self, schema: AddGoodSchema) -> Good:
        return super().add(schema)

    def update(
        self, id: int, schema: UpdateGoodSchema | UpdateGoodEmbeddingsSchema
    ) -> Good:
        return super().update(id, schema)

    def delete(self, id: int) -> Good:
        return super().delete(id)
