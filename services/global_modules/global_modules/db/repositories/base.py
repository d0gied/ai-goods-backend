from abc import ABC, abstractmethod
from typing import Type, Union

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models.base import Base
from ..schemas.base import AddSchemaType, UpdateSchemaType


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Union[Base, None]:
        pass

    @abstractmethod
    def get_all(self) -> list[Base]:
        pass

    @abstractmethod
    def add(self, schema: AddSchemaType) -> Base:
        pass

    @abstractmethod
    def add_many(self, schemas: list[AddSchemaType]) -> list[Base]:
        pass

    @abstractmethod
    def update(self, id: int, schema: UpdateSchemaType) -> Base:
        pass

    @abstractmethod
    def delete(self, id: int) -> Base:
        pass


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base] = None

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get(self, id: int) -> Union[Base, None]:
        return self.session.get(self.model, id)

    def get_all(self) -> list[Base]:
        return self.session.query(self.model).all()

    def add(self, schema: AddSchemaType) -> Base:
        instance = self.model(**schema.model_dump())
        self.session.add(instance)
        return instance

    def add_many(self, schemas: list[AddSchemaType]) -> list[Base]:
        instances = [self.model(**schema.model_dump()) for schema in schemas]
        self.session.add_all(instances)
        return instances

    def update(self, id: int, schema: UpdateSchemaType) -> Base:
        instance = self.session.get(self.model, id)
        if instance is None:
            raise ValueError(f"Instance with id={id} not found")

        for field, value in schema.model_dump().items():
            setattr(instance, field, value)

        return instance

    def delete(self, id: int) -> Base:
        instance = self.session.get(self.model, id)
        self.session.delete(instance)
        return instance

    def get_by_ids(self, ids: list[int]) -> list[Base]:
        return self.session.query(self.model).filter(self.model.id.in_(ids)).all()
