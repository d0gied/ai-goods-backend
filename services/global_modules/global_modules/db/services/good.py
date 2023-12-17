from ..models import Good, Image
from ..repositories.good import GoodRepository
from ..repositories.image import ImageRepository
from ..schemas.good import (
    AddGoodSchema,
    AddImageSchema,
    UpdateGoodEmbeddingsSchema,
    UpdateGoodSchema,
)
from ..uow import UnitOfWork


class GoodService:
    def __init__(self, uow: UnitOfWork = None):
        if uow is None:
            uow = UnitOfWork()
        self.uow = uow

    def add(self, schema: AddGoodSchema) -> Good:
        with self.uow:
            image_urls = schema.images
            schema.images = []
            good = self.uow.goods.add(schema)
            self.uow.commit()
            self.uow.refresh(good)

            if image_urls is not None:
                image_schemas = [
                    AddImageSchema(url=url, good_id=good.id) for url in image_urls
                ]
                self.uow.images.add_many(image_schemas)
                self.uow.commit()
                self.uow.refresh(good)

            return good

    def add_many(self, schemas: list[AddGoodSchema]) -> list[Good]:
        with self.uow:
            image_urls = []

            for schema in schemas:
                image_urls.append(schema.images)
                schema.images = []

            goods = self.uow.goods.add_many(schemas)
            self.uow.commit()
            self.uow.refresh_all(goods)

            for good, urls in zip(goods, image_urls):
                if urls is not None:
                    image_schemas = [
                        AddImageSchema(url=url, good_id=good.id) for url in urls
                    ]
                    self.uow.images.add_many(image_schemas)

            self.uow.commit()
            self.uow.refresh_all(goods)
            self.uow.session.expunge_all()
            return goods

    def get(self, good_id: int) -> Good:
        with self.uow:
            good = self.uow.goods.get(good_id)
            return good

    def get_by_source_id(self, id: str, source: str) -> Good:
        return self.get_by_source_ids([id], source)[0]

    def get_by_source_ids(self, ids: list[str], source: str) -> list[Good]:
        with self.uow:
            goods = self.uow.goods.get_by_source_ids(source, ids)
            return goods

    def get_by_ids(self, ids: list[int]) -> list[Good]:
        with self.uow:
            goods = self.uow.goods.get_by_ids(ids)
            return goods

    def get_all(self) -> list[Good]:
        with self.uow:
            goods = self.uow.goods.get_all()
            return goods
