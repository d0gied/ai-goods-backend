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

    def add_many(self, schemas: list[AddGoodSchema]) -> list[Good]:
        return super().add_many(schemas)

    def update(
        self, id: int, schema: UpdateGoodSchema | UpdateGoodEmbeddingsSchema
    ) -> Good:
        return super().update(id, schema)

    def delete(self, id: int) -> Good:
        return super().delete(id)

    def get_by_ids(self, ids: list[int]) -> list[Good]:
        return super().get_by_ids(ids)

    def get_by_source_ids(self, source: str, ids: list[str] | list[int]) -> list[Good]:
        ids = [str(id) for id in ids]
        with SessionLocal() as session:
            return (
                session.query(self.model)
                .filter(self.model.source == source, self.model.source_id.in_(ids))
                .all()
            )
