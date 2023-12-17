from unittest.mock import patch

import pytest
from global_modules.db.models import Good
from global_modules.db.repositories import AbstractRepository, GoodRepository
from global_modules.db.schemas import AddGoodSchema, UpdateGoodSchema


class MockSQLAlchemyRepo(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.repo: dict[Good] = {}

    def get(self, id: int):
        return self.repo.get(id)

    def get_all(self) -> list[Good]:
        return list(self.repo.values())

    def add(self, schema: AddGoodSchema):
        good = Good(**schema.model_dump())
        good.id = len(self.repo) + 1
        self.repo[good.id] = good
        return good

    def add_many(self, schemas: list[AddGoodSchema]):
        goods = [Good(**schema.model_dump()) for schema in schemas]
        for good in goods:
            good.id = len(self.repo) + 1
            self.repo[good.id] = good
        return goods

    def update(self, id: int, schema: UpdateGoodSchema):
        good: Good = self.repo[id]
        for key, value in schema.model_dump().items():
            setattr(good, key, value)
        return good

    def delete(self, id: int):
        return self.repo.pop(id)


@pytest.fixture(scope="class", autouse=True, name="repo")
def fixture_good_repository() -> AbstractRepository:
    return MockSQLAlchemyRepo()


# def test_add_good(repo: MockSQLAlchemyRepo):
#     # sourcery skip: extract-duplicate-method
#     good_schema = AddGoodSchema(name="test", price=10)
#     good = repo.add(good_schema)
#     assert good.id == 1
#     assert good.name == "test"
#     assert good.price == 10


# def test_get_good(repo: MockSQLAlchemyRepo):
#     good_schema = AddGoodSchema(name="test", price=10)
#     good = repo.add(good_schema)
#     good = repo.get(good.id)
#     assert good.id == 1
#     assert good.name == "test"
#     assert good.price == 10


# def test_update_good(repo: MockSQLAlchemyRepo):
#     good_schema = AddGoodSchema(name="test", price=10)
#     good = repo.add(good_schema)
#     good_schema = UpdateGoodSchema(name="test2", price=20)
#     good = repo.update(good.id, good_schema)
#     assert good.id == 1
#     assert good.name == "test2"
#     assert good.price == 20


# def test_delete_good(repo: MockSQLAlchemyRepo):
#     good_schema = AddGoodSchema(name="test", price=10)
#     good = repo.add(good_schema)
#     good = repo.delete(good.id)
#     assert good.id == 1
#     assert good.name == "test"
#     assert good.price == 10
#     assert len(repo.repo) == 0
